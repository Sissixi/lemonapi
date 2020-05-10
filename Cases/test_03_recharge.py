"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/8 0008下午 9:03
"""
import unittest
from libs.ddt import ddt, data
from Commons.handle_excel import HandleExcel
from Commons.handle_yaml import do_yaml
from Commons.handle_logs import do_log
from Commons.handle_requests import HandleRequests
from Commons.handle_parameterized import Parameterization
from Commons.handle_mysql import HandleMysql


@ddt
class TestRecharge(unittest.TestCase):
    do_excel = HandleExcel('recharge')
    cases = do_excel.read_excel()

    @classmethod
    def setUpClass(cls) -> None:
        # 创建发起请求对象
        cls.do_request = HandleRequests()
        cls.do_request.add_headers(do_yaml.read_yaml("api", "version"))
        # 创建sql对象
        cls.do_sql = HandleMysql()

    @classmethod
    def tearDownClass(cls) -> None:
        # 关闭会话
        cls.do_request.close()
        # 关闭连接
        cls.do_sql.close()

    @data(*cases)
    def test_recharge(self, case):
        # 获取参数data
        new_data = Parameterization.to_param(case.data)
        # 获取url
        new_url = do_yaml.read_yaml("api", "base_url") + case.url
        # check_sql
        check_sql = case.check_sql
        # 充值前获取用户金额
        if check_sql:
            check_sql = Parameterization.to_param(check_sql)
            mysql_data = self.do_sql.run(check_sql)
            before_amount = round(float(mysql_data['leave_amount']), 2)
        # 发起请求
        res = self.do_request.send(url=new_url, data=new_data)
        # 请求数据转化为dict格式
        actual = res.json()
        # 获取title
        title = case.title
        # 获取行数
        row = case.case_id + 1
        # 期望值的获取
        expcted = case.expected
        # 获取登录接口的token
        if case.case_id == 2:
            token = actual["data"]["token_info"]["token"]
            # 更新请求头
            self.do_request.add_headers(
                {"Authorization": "Bearer " + token}
            )
        try:
            self.assertEqual(expcted, actual.get('code'), msg=title)
            # 充值后获取用户金额
            if check_sql:
                mysql_data = self.do_sql.run(check_sql)
                after_amount = round(float(mysql_data['leave_amount']), 2)
                # 实际相差金额--数据库中计算的相差的金额
                value = round(float(after_amount - before_amount), 2)
                # 期望的金额
                expcted_amount = eval(new_data)["amount"]
                self.assertEqual(expcted_amount, value)
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
