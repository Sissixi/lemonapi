"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/10 0010下午 1:20
"""
import unittest
from libs.ddt import ddt, data
from Commons.handle_parameterized import Parameterization
from Commons.handle_requests import HandleRequests
from Commons.handle_yaml import do_yaml
from Commons.handle_excel import HandleExcel
from Commons.handle_logs import do_log


@ddt
class TestAdd(unittest.TestCase):
    # 创建excel对象
    do_excel = HandleExcel('add')
    # 读取excel
    cases = do_excel.read_excel()

    @classmethod
    def setUpClass(cls) -> None:
        # 创建会话对象
        cls.do_requests = HandleRequests()
        # 添加请求头
        cls.do_requests.add_headers(do_yaml.read_yaml("api", "version"))

    @classmethod
    def tearDownClass(cls) -> None:
        # 关闭会话
        cls.do_requests.close()

    @data(*cases)
    def test_add(self, case):
        # 获取请求数据data
        new_data = Parameterization.to_param(case.data)
        # 获取url
        new_url = do_yaml.read_yaml('api', 'base_url') + case.url
        # 发起请求
        res = self.do_requests.send(url=new_url, data=new_data)
        # 转化为字典格式
        actual_res = res.json()
        # 获取预期结果
        expected_res = case.expected
        # 获取行数
        row = case.case_id + 1
        # 获取标题
        msg = case.title
        # 获取token
        if case.case_id == 2:
            token = actual_res["data"]["token_info"]["token"]
            # 更新请求头
            self.do_requests.add_headers({"Authorization": "Bearer " + token})

        try:
            self.assertEqual(expected_res, actual_res.get('code'), msg=msg)
        except AssertionError as e:
            do_log.error(f"用例{msg}:执行失败")
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'result_col'),
                                      value=do_yaml.read_yaml('excel', 'nopass'))
            raise e
        else:
            do_log.error(f"用例{msg}:执行成功")
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'result_col'),
                                      value=do_yaml.read_yaml('excel', 'pass'))
        finally:
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'actual_col'),
                                      value=res.text)


if __name__ == '__main__':
    unittest.main()
