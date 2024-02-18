import yaml
import io
import ruamel
import os
import configparser


def read_yaml(file_path):
    """
    读取YAML文件并解析为结构化的字典类型
    @param file_path: (str) 文件路径
    @return: (dict) 解析文件内容
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def read_yaml_with_comments(yaml_path):
    # 创建yaml解析器实例，并设置保留注释
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.allow_duplicate_keys = True  # 允许重复键以保留注释

    # 打开并读取yaml文件
    with open(yaml_path, 'r') as file:
        data = yaml.load(file)

    # 创建一个新的字符串IO对象用于存储包含注释的YAML文本
    output_str = io.StringIO()

    # 将数据写入新的字符串IO对象，并获取原始、包含注释的YAML字符串
    yaml.dump(data, output_str)
    yaml_text = output_str.getvalue()

    return yaml_text


def write_yaml_with_comments(yaml_path, data=None):
    # 创建yaml解析器实例，并设置保留注释
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.indent(sequence=4, offset=2)
    yaml.allow_duplicate_keys = True  # 允许重复键以保留注释

    # 检查data是否为包含注释的YAML格式字符串
    if isinstance(data, str):
        # 将数据（包含注释）重新写入到指定输出文件中
        with open(yaml_path, 'w') as outfile:
            outfile.write(data)
    else:
        # 如果data不是字符串，则认为是要写入空字典或默认内容
        with open(yaml_path, 'w') as outfile:
            if not data:
                yaml.dump("", outfile)
            else:
                yaml.dump(data, outfile)


import ruamel.yaml


def is_valid_yaml(yaml_string):
    try:
        yaml = ruamel.yaml.YAML(typ='safe', pure=True)
        # 尝试解析字符串
        yaml.load(yaml_string)
        return True  # 如果没有抛出异常，则认为是有效的YAML
    except ruamel.yaml.YAMLError:
        return False  # 如果抛出了YAMLError，则说明不是有效的YAML格式


def list_all_yaml_files_in_directory(directory_path):
    # 从给定的文件路径列表中筛选出.yaml文件，并返回包含这些文件路径的新列表。
    yaml_file_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.yaml'):  # or file.endswith('.yml')
                # 继续完成路径的拼接并添加到列表中
                yaml_file_paths.append(os.path.join(root, file))
    return yaml_file_paths


def yaml_files_content(yaml_files):
    # 定义一个函数，用于获取所有YAML文件的内容并返回一个内容列表
    content_list = []  # 创建一个空列表，用于存储所有YAML文件的内容
    # 遍历每个YAML文件
    for yaml_file in yaml_files:
        read_data = read_yaml(yaml_file)  # 读取YAML文件的内容
        if read_data is None:  # 如果读取失败，则跳过当前文件
            continue
        content_list.append(read_data)  # 将当前YAML文件的内容添加到内容列表中

    return content_list  # 返回所有YAML文件的内容列表


class ConfigManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.config = configparser.ConfigParser()
        # 读取INI文件
        self.config.read(self.filepath)

    def set_value(self, section, option, value):
        # 修改指定section和option的值
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

        # 将修改后的配置写回文件
        with open(self.filepath, 'w') as configfile:
            self.config.write(configfile)
