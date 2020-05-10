"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/5 0005上午 7:20
"""
import unittest
import os
from HTMLTestRunnerNew import HTMLTestRunner
from datetime import datetime
from Commons.handle_yaml import do_yaml
from Commons.handle_path import REPORT_DIR,USER_DATA,CASE_DIR
from Commons.handle_user import new_data
#如果用户账号文件,不存在就创建
if not os.path.exists(USER_DATA):
    new_data()

# # 创建测试套件
# suite = unittest.TestSuite()
# # 测试用例加载到测试套件中
# loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(test_01_register))
suite=unittest.defaultTestLoader.discover(CASE_DIR)
# 测试运行程序
# 报告名
filename = do_yaml.read_yaml('report', 'reportname') + "_" + \
           datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + '.html'
# 报告路径
file_path = os.path.join(REPORT_DIR, filename)
with open(file_path, 'wb')as file:
    runner = HTMLTestRunner(stream=file,
                            title=do_yaml.read_yaml('report', 'title'),
                            description=do_yaml.read_yaml('report', 'description'),
                            tester=do_yaml.read_yaml('report', 'tester')
                            )
    # 测试运行
    runner.run(suite)
