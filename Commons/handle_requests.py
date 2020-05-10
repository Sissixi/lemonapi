"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/5 0005上午 7:26
"""
import requests
import json
from Commons.handle_logs import do_log


class HandleRequests:
    def __init__(self):
        # 创建一个会话对象，这个会话对象自动传递cookies信息
        self.one_session = requests.Session()

    def add_headers(self, headers):
        # 添加公共请求头
        self.one_session.headers.update(headers)

    def send(self, url, method='post', data=None, is_json=True, **kwargs):
        # 先判断data是否为字符串格式
        if isinstance(data, str):
            try:
                # 如果是 json格式的字符串，使用loads转化为python字典
                data = json.loads(data)
            except Exception as e:
                # 如果是 字典格式的字符串，使用eval转化为python字典
                data = eval(data)
                do_log.error(f"传递参数{data}格式不是json格式的字符串")

        # 所有传递的方式全部小写
        method = method.lower()
        # 如果请求方法是get,传递的参数就是params查询字符串参数，get没有请求体
        if method == 'get':
            res = self.one_session.request(method, url, params=data, **kwargs)
        # 如果请求方法是"post","put","delect","patch",这些请求有请求体，可以传json,或者form表单
        elif method in ("post", 'put', 'delect', 'patch'):
            if is_json:
                # 如果is_json为true，就以json格式传递参数
                res = self.one_session.request(method, url, json=data, **kwargs)
            else:
                # 如果is_json为false，就以form表单传递参数
                res = self.one_session.request(method, url, data=data, **kwargs)
        else:
            res = None
            do_log.error(f"不支持的请求方法{method}")
        # 返回Response响应报文对象
        return res

    def close(self):
        # 关闭会话，释放资源；还可以发起请求
        self.one_session.close()
