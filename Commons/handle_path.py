"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/5 0005下午 7:57
"""
import os
#获取项目跟路径
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#获取配置文件夹所在路径
CONFIGS_DIR=os.path.join(BASE_DIR,'configs')
#获取配置文件所在路径
CONFIG_FILE_PATH=os.path.join(CONFIGS_DIR,'testcase.yaml')
#获取日志文件所在的目录路径
LOGS_DIR=os.path.join(BASE_DIR,'logs')
#获取报告文件所在目录的路径
REPORT_DIR=os.path.join(BASE_DIR,'reports')
#获取excel所在目录路径
DATAS_DIR=os.path.join(BASE_DIR,'datas')
#获取用户信息路径
USER_DATA=os.path.join(CONFIGS_DIR,'user_info.yaml')
#用例模块所在类
CASE_DIR=os.path.join(BASE_DIR,'Cases')