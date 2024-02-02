import importlib
from tornado.web import url

from util.file import list_all_yaml_files_in_directory, read_yaml


# 获取所有路由
def get_all_routes(directory):
    """
    初始化路由
    :param directory: (str) API文件夹路径
    :return urlpatterns: (list) 路由规则列表
    """
    yaml_files = list_all_yaml_files_in_directory(directory)
    urlpatterns = []
    for file in yaml_files:
        content = read_yaml(file)
        uri = content.get("Uri")  # 获取URI
        handler = content.get("Handler")  # 获取处理器
        if uri is None:
            raise Exception("No Uri in %s", file)
        if handler is None:
            raise Exception("No Handler in %s", file)
        module_path, class_name = handler.rsplit('.', 1)  # 分离出模块路径和类名
        module = importlib.import_module(module_path)  # 动态导入模块
        cls = getattr(module, class_name)  # 获取模块中的类
        urlpatterns += [url(uri, cls)]  # 添加路由规则到列表中
    return urlpatterns  # 返回路由规则列表
