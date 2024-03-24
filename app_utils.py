import random
import string

def generate_random_string(length=10):
    """随机字符串生成

    Args:
        length (int, optional): 字符串长度. Defaults to 10.

    Returns:
        str: _description_
    """    
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def insert_random_string_to_filename(filename, random_string):
    """重构图片名

    Args:
        filename (str): 图片名称

    Returns:
        str: _description_
    """    
    file_name, file_extension = filename.rsplit('.', 1)
    #random_string = generate_random_string()
    return f"{file_name}-nex{random_string}.{file_extension}"