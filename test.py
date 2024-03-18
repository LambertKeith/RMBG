from config import get_config
from app_utils import generate_random_string

def test1():
    print(get_config.read_yaml_file())


def test2():
    pic_path_dict = {
        'source_pic': 'source_path',
        'output_pic': 'output_path'
    }
    if 'source_pic' in pic_path_dict:
        print("yes")


def test3():
    print(generate_random_string())
    pass

if __name__ == "__main__":
     test3()
    
    