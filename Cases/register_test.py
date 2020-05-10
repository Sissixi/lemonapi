"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/5 0005上午 7:24
"""
import unittest
from Commons.handle_excel import HandleExcel
from libs.ddt import ddt, data
from Cases.register import register
from Commons.handle_yaml import do_yaml
from Commons.handle_logs import do_log


@ddt
class RegistersTest(unittest.TestCase):
    do_excel = HandleExcel('registers')
    cases = do_excel.read_excel()

    @data(*cases)
    def test_register_case(self, case):
        # 获取data
        data = eval(case.data)
        # 获取期望结果
        expected = eval(case.expected)
        # 获取行数
        row = case.case_id + 1
        # 实际结果
        res = register(*data)
        try:
            self.assertEqual(expected, res)
        except AssertionError as e:
            do_log.error(f"测试用例:{case.title}-执行失败，失败原因{e}")
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'column'),
                                      value=do_yaml.read_yaml('excel', 'nopass'))

            raise e

        else:
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'column'),
                                      value=do_yaml.read_yaml('excel', 'pass'))
            do_log.info(f"测试用例:{case.title}-执行成功")
