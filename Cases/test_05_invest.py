"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/10 0010下午 12:44
"""
import unittest
import json
from libs.ddt import ddt, data
from Commons.handle_excel import HandleExcel
from Commons.handle_logs import do_log
from Commons.handle_yaml import do_yaml
from Commons.handle_requests import HandleRequests
from Commons.handle_parameterized import Parameterization
from Commons.handle_mysql import HandleMysql
'''接口依赖'''
@ddt
class TestInvest(unittest.TestCase):
    # 获取excel对象
    do_excel = HandleExcel("invest")
    # 读取excel
    cases = do_excel.read_excel()

    @classmethod
    def setUpClass(cls) -> None:
        # 开启会话
        cls.do_requests = HandleRequests()
        #创建sql
        cls.do_sql=HandleMysql()
        # 添加请求头
        cls.do_requests.add_headers(do_yaml.read_yaml('api', 'version'))
    @classmethod
    def tearDownClass(cls) -> None:
        # 关闭会话
        cls.do_requests.close()
        #关闭sql
        cls.do_sql.close()

    @data(*cases)
    def test_invest(self, case):
        # 获取参数data,先参数化
        new_data = Parameterization.to_param(case.data)
        # 拼接完整的url
        new_url = do_yaml.read_yaml('api', 'base_url') + case.url
        # 向服务器发起请求
        res = self.do_requests.send(url=new_url,
                                    method=case.method,
                                    data=new_data,
                                    is_json=True)
        # 将响应的报文格式转为字典
        actual_value = res.json()
        # 获取期望结果,是int无需转化
        expected_result = case.expected
        # 获取title
        msg = case.title
        # 获取用例行数
        row = case.case_id + 1
        # 获取用例执行成功提示
        success_msg = do_yaml.read_yaml('excel', 'pass')
        # 获取用例执行失败提示
        fail_msg = do_yaml.read_yaml('excel', 'nopass')
        # 预期结果与实际结果进行 断言
        try:
            self.assertEqual(expected_result, actual_value.get("code"), msg=msg)
        except AssertionError as e:
            # 断言失败执行的代码
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'result_col'),
                                      value=fail_msg)
            do_log.error(f"用例:{msg}执行失败,失败原因{e}")
            raise e
        else:
            # 断言成功获取token
            if 'token_info' in res.text:
                token = actual_value["data"]["token_info"]["token"]
                # 更新请求头
                self.do_requests.add_headers({"Authorization": "Bearer " + token})
            #获取load_id
            check_sql=case.check_sql
            if check_sql:
                check_sql=Parameterization.to_param(check_sql)
                load_id=self.do_sql.run(check_sql)
                load_id=load_id['id']
                setattr(Parameterization,'load_id',load_id)
            #第二种方法-处理多个sql，定义为json
            #
            # check_sql=json.loads(case.check_sql,encoding='utf8')
            # if "load_id" in check_sql:
            #     check_sql = Parameterization.to_param(check_sql)
            #     load_id = self.do_sql.run(check_sql)
            #     load_id = load_id['id']
            #     setattr(Parameterization, 'load_id', load_id)



            # 断言成功执行的代码
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'result_col'),
                                      value=success_msg)
            do_log.info(f"用例:{msg}执行成功")
        finally:
            # 写入实际值
            self.do_excel.write_excel(row=row,
                                      column=do_yaml.read_yaml('excel', 'actual_col'),
                                      value=res.text)


if __name__ == '__main__':
    unittest.main()
