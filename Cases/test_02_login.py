"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/7 0007下午 10:48
"""
import unittest
from libs.ddt import ddt, data
from Commons.handle_excel import HandleExcel
from Commons.handle_logs import do_log
from Commons.handle_requests import HandleRequests
from Commons.handle_parameterized import Parameterization
from Commons.handle_yaml import do_yaml
'''多字段断言'''
@ddt
class TestLogin(unittest.TestCase):
    # 获取excel对象
    do_excel = HandleExcel("login")
    # 读取excel
    cases = do_excel.read_excel()

    @classmethod
    def setUpClass(cls) -> None:
        # 开启会话
        cls.do_requests = HandleRequests()
        # 添加请求头
        cls.do_requests.add_headers(do_yaml.read_yaml("api", "version"))

    @classmethod
    def tearDownClass(cls) -> None:
        # 关闭会话
        cls.do_requests.close()

    @data(*cases)
    def test_login(self, case):
        # 获取参数data
        new_data = Parameterization.to_param(case.data)
        # 获取new_url
        new_url = do_yaml.read_yaml('api', 'base_url') + case.url
        # 向登录接口发起请求
        res = self.do_requests.send(url=new_url, data=new_data)
        # 转为字典格式的数据
        actual = res.json()
        # 获取预期结果,期望值是json格式字符串，使用eval转化
        expcted = eval(case.expected)
        # 获取行数
        row = case.case_id + 1
        # 获取title
        title = case.title
        try:
            self.assertEqual(expcted.get('code'), actual.get('code'), msg=title)
            self.assertEqual(expcted.get('msg'), actual.get('msg'), msg=title)
        except AssertionError as e:
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'result_col'),
                                      value=do_yaml.read_yaml('excel', 'nopass'))
            do_log.error(f"用例{title}:执行失败，原因为{e}")
            raise e
        else:
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'result_col'),
                                      value=do_yaml.read_yaml('excel', 'pass'))
            do_log.info(f"用例{title}:执行成功")
        finally:
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'actual_col'),
                                      value=res.text)
if __name__ == '__main__':
    unittest.main()