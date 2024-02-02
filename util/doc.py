import json

from util.file import yaml_files_content, list_all_yaml_files_in_directory
import os

from util.proc import run_command_in_directory


def to_doc_table(data, api_type="@apiParam"):
    """
    :param data: (dict) 要转换的数据
    :param api_type: (str) apidoc类型 @apiParam请求参数 请求成功响应@apiSuccess
    :return: api_param (str) apidoc表格格式数据
    """
    results = []  # 存储结果列表

    def traverse_dict(d, current_path=None):  # 遍历字典函数
        if d is None:
            return
        for key, value in d.items():  # 遍历字典的键值对
            v_type = value.get('type')  # 获取value的type属性
            add_data = {
                "path": '',
                "key": key,
                "value": value,
                "desc": value.get("desc"),
                "type": v_type
            }
            if v_type == 'object':  # 如果type为object
                new_path = current_path + (key,) if current_path is not None else (key,)  # 生成新的路径
                add_data["path"] = new_path
                results.append(add_data)  # 将路径、键、值为空字典、描述添加到结果列表
                if 'params' in value:  # 如果value中有'params'键
                    traverse_dict(value['params'], new_path)  # 递归调用traverse_dict函数
            elif v_type == 'array':  # 如果type为array
                new_path = current_path + (key,) if current_path is not None else (key,)  # 生成新的路径
                add_data["path"] = new_path
                results.append(add_data)  # 将路径、键、值为空列表、描述添加到结果列表
                a_params = value.get("items", {}).get("params", {})  # 获取value的items中的params
                traverse_dict(a_params, new_path)  # 递归调用traverse_dict函数
            else:  # 其他情况
                new_path = current_path + (key,) if current_path is not None else (key,)  # 生成新的路径
                add_data["path"] = new_path
                results.append(add_data)  # 将路径、键、值、描述添加到结果列表

    traverse_dict(data)  # 调用traverse_dict函数遍历字典

    api_param = ''  # 初始化api_param为空字符串
    for item in results:  # 遍历结果列表
        full_parent = '.'.join(item.get("path"))  # 将路径列表通过.连接成字符串
        desc = item.get('desc')  # 获取描述
        data_type = item.get("type")  # 获取数据类型
        api_param += f'{api_type}  {{{data_type}}} {full_parent} {desc} \n'  # 拼接api_param字符串
    return api_param  # 返回api_param字符串


def type_default_values(v_type):
    """
        根据给定的数据类型返回对应类型的默认值
        :param v_type: (str)  数据类型
        :return:    默认值  根据数据类型的不同返回对应的默认值
        """
    if v_type == "string":
        return ""
    elif v_type == "object":
        return {}
    elif v_type == "array":
        return []
    elif v_type == "bool":
        return False
    elif v_type == "number":
        return 0
    return None


def to_doc_default_example(d):
    """
    生成默认值
    :param d: (dict)
    :return: (dict)
    """
    if d is None:
        return
    result = {}
    for key, value in d.items():
        v_type = value.get('type')
        if v_type == 'object':
            nested_result = to_doc_default_example(value['params'])
            result[key] = nested_result
        elif v_type == 'array':
            item_type = value.get('items', {}).get('type')
            default_array_item = type_default_values(item_type)
            array_result = [default_array_item]
            if 'params' in value['items']:
                nested_item = to_doc_default_example(value['items']['params'])
                array_result = [nested_item]
            result[key] = array_result
        else:
            result[key] = type_default_values(v_type)
    return result


def to_doc_example(data, space=4):
    """
    :param data: (dict) 要转换的数据
    :param space: (int) 在每行前面添加space个空格
    :return: (str)
    """
    example_data = to_doc_default_example(data)
    formatted_json = json.dumps(example_data, indent=space)
    indented_json = ''.join([' ' * space + line for line in formatted_json.splitlines(True)])
    return indented_json


def write_to_file(directory, write_file):
    """
    将文件内容写入指定文件
    参数:
     :param directory: (str): 目录路径
     :param write_file: (str): 写入的文件名
     :return: None
     """
    yaml_files = list_all_yaml_files_in_directory(directory)
    files_content_list = yaml_files_content(yaml_files)
    write_cont = ''
    for content in files_content_list:
        uri = content.get("Uri")
        group = content.get("Group")
        for detail in content.get("Details", []):
            if detail is None:
                continue
            desc = detail.get("Desc")
            method = detail.get("Method")
            write_cont += '"""\n'
            write_cont += f'@api {{{method}}} {uri} {desc} \n'
            write_cont += f'@apiName {desc} \n'
            write_cont += f'@apiGroup {group} \n'
            req_params = detail.get("ReqParam", {}).get("params")
            res_params = detail.get("ResParam", {}).get("params")
            if req_params:  # 请求格式化
                write_cont += to_doc_table(req_params)
                write_cont += '\n'
                write_cont += '@apiParamExample {json} Request-Example:\n'
                write_cont += to_doc_example(req_params)
                write_cont += '\n'
            if res_params:  # 响应格式化
                write_cont += to_doc_table(res_params, "@apiSuccess")
                write_cont += '\n'
                write_cont += '@apiSuccessExample Success-Response:\n'
                write_cont += to_doc_example(res_params)
                write_cont += '\n'
            write_cont += '"""\n'
    with open(write_file, "w") as f:
        f.write(write_cont)


def write_doc_json(write_file, name="squirrellib", desc="REST API"):
    """
    生成doc.json文件
    @param write_file: (str) 文件路径
    @param name: (str) 文档名称
    @param desc: (str) 文档描述
    @return: Node
    """
    data = {
        "name": name,
        "description": desc
    }
    with open(write_file, "w") as f:
        json.dump(data, f)


apis_dir = os.getcwd() + '/apis'
doc_dir = os.getcwd() + '/__apidoc'


def generate_doc(apis_dir_path=apis_dir, doc_dir_path=doc_dir):
    """
    生成doc文件
    """
    # 目录创建
    os.makedirs(doc_dir_path, exist_ok=True)
    # 配置文件生成
    write_doc_json(f'{doc_dir_path}/apidoc.json')
    write_to_file(apis_dir_path, f'{doc_dir_path}/doc.py')
    # 生成文档
    cmd = f'apidoc -i {doc_dir_path} -o {doc_dir_path}'
    run_command_in_directory(doc_dir_path, cmd)
