import yaml

def read_yaml_file(file_path='config/rmbg_config.yaml'):
    """读取配置文件

    Args:
        file_path (str, optional): 配置文件路径. Defaults to 'config/rmbg_config.yaml'.

    Returns:
        _type_: 配置内容
    """    
    try:
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
            return content['rmbg']
    except Exception as e:
        print(f"Failed to read YAML file: {e}")
        return None

# 示例用法
""" file_path = "example.yaml"
data = read_yaml_file(file_path)
if data:
    print(data)
 """