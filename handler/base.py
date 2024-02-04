# 基础类 配置跨域
import tornado.web
import json
from json import JSONEncoder


# 声明基类

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)

    def set_default_headers(self):
        """
        设置请求头信息
        """
        # 设置请求头信息
        # 域名信息
        self.set_header("Access-Control-Allow-Origin", "*")
        # 请求信息
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        # 请求方式
        self.set_header("Access-Control-Allow-Methods", "POST,GET,PUT,DELETE,TRACE,HEAD,PATCH,OPTIONS")

    def finish(self, chunk=None):
        """
        完成响应
        :rtype: object
        """
        if chunk is not None and not isinstance(chunk, bytes):
            chunk = json.dumps(chunk, indent=4, sort_keys=True, default=str, ensure_ascii=False)
        try:
            tornado.web.RequestHandler.write(self, chunk)
        except JSONEncoder as e:
            pass
        tornado.web.RequestHandler.finish(self)

    def json_response(self, code, msg, **kwargs):
        """
        完成响应
        :param code: 状态码
        :param msg: 状态信息
        :param kwargs: 其他参数
        :return: object
        """
        return self.finish({"code": code, "msg": msg, **kwargs})

    def get_json_body(self):
        """
        获取请求体中的JSON数据
        :return: object
        """
        try:
            body = self.request.body.decode('utf-8')  # 将请求体从字节串转换为字符串（假设编码为UTF-8）
            json_data = json.loads(body)  # 解析JSON字符串为Python对象
            return json_data
        except (json.JSONDecodeError, AttributeError):  # 捕获JSON解析错误或请求对象可能没有body属性的情况
            return {}  # 或者抛出一个异常，取决于你的具体需求和应用的上下文

    def post(self):
        """
        处理POST请求
        """
        self.write("这里是post请求")

    def trace(self):
        """
        处理TRACE请求
        """
        self.write("这里是trace请求")

    def get(self):
        """
        处理GET请求
        """
        self.write("这里是get请求")

    def put(self):
        """
        处理PUT请求
        """
        self.write("这里是put请求")

    def head(self):
        """
        处理HEAD请求
        """
        self.write("这里是head请求")

    def delete(self):
        """
        处理DELETE请求
        """
        self.write("这里是delete请求")

    def patch(self):
        """
        处理PATCH请求
        """
        self.write("这里是patch请求")

    def options(self, *args):
        """
        处理OPTIONS请求
        """
        # 设置状态吗
        self.set_status(204)
        self.finish()
