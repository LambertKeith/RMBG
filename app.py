from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from skimage import io
import torch
from PIL import Image
from briarmbg import BriaRMBG
from utilities import preprocess_image, postprocess_image
from huggingface_hub import hf_hub_download
import os
from pydantic import BaseModel
import shutil
from config.get_config import read_yaml_file
import app_utils as a_utils


source_path = read_yaml_file()["source_path"]
output_path = read_yaml_file()["output_path"]

app = FastAPI()


@app.post("/rmbg/")
async def rmbg(file: UploadFile = File(...)):
    """删除传入图片的背景

    Args:
        file (UploadFile, optional): 传入图片. Defaults to File(...).

    Raises:
        HTTPException: 报错返回

    Returns:
        str: 文件返回路径
    """    

    # 防重名处理
    #为每个图片名加上随机字符
    random_str = a_utils.generate_random_string()
    filename = a_utils.insert_random_string_to_filename(file.filename, random_str) 

    try:
        # Save uploaded file
        file_path = f"{os.path.dirname(os.path.abspath(__file__))}/{source_path}/{filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Load pre-trained model
        net = BriaRMBG.from_pretrained("briaai/RMBG-1.4")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        net.to(device)
        net.eval()

        # Prepare input
        model_input_size = [1024,1024]
        orig_im = io.imread(file_path)
        orig_im_size = orig_im.shape[0:2]
        image = preprocess_image(orig_im, model_input_size).to(device)

        # Inference 
        result = net(image)

        # Post process
        result_image = postprocess_image(result[0][0], orig_im_size)

        # Save result
        pil_im = Image.fromarray(result_image)
        no_bg_image = Image.new("RGBA", pil_im.size, (0,0,0,0))
        orig_image = Image.open(file_path)
        no_bg_image.paste(orig_image, mask=pil_im)
        result_file_path = f"{os.path.dirname(os.path.abspath(__file__))}/{output_path}/{os.path.splitext(filename)[0]}_no_bg.png"
        no_bg_image.save(result_file_path)

        # Return the result file
        return FileResponse(result_file_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


pic_path_dict = {
    'source_pic': source_path,
    'output_pic': output_path
}


@app.post("/pic_clean/")
def source_clean(clean_targat: str):
    """_summary_

    Args:
        clean_targat (str): 清理文件的目录

        源文件目录：source_pic

        处理后目录：output_pic

        注意不能有空格

    Returns:
        _type_: _description_
    """    
    if clean_targat in pic_path_dict:
        folder_path = f'{os.path.dirname(os.path.abspath(__file__))}/{pic_path_dict[clean_targat]}'
    else:
        return HTTPException(status_code=500, detail='没有找到文件夹')

    info = 'operate success'
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
    
    return info

