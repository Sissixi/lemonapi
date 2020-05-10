"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/5 0005上午 7:25
"""
import logging
import os
from Commons.handle_path import LOGS_DIR
from Commons.handle_yaml import do_yaml


class HandleLogs:
    @classmethod
    def create_log(cls):
        # 自定义一个日志收集器
        mylog = logging.getLogger(do_yaml.read_yaml('logs', 'logname'))
        # 设置日志收集器等级
        mylog.setLevel(do_yaml.read_yaml('logs', 'logleval1'))
        # 设置输出格式
        formatted = logging.Formatter(do_yaml.read_yaml('logs', 'formated'))
        '''设置输出到控制台'''
        sh = logging.StreamHandler()
        # 设置输出等级
        sh.setLevel(do_yaml.read_yaml('logs', 'logleval2'))
        # 将输出到控制台添加到日志收集器中
        mylog.addHandler(sh)
        # 设置输出格式
        sh.setFormatter(formatted)
        '''设置输出到文件'''
        fl = logging.FileHandler(filename=os.path.join(LOGS_DIR, do_yaml.read_yaml('logs', 'logfilename')),
                                 encoding='utf8')
        # 设置输出等级
        fl.setLevel(do_yaml.read_yaml('logs', 'logleval2'))
        # 设置输出到文件添加到日志收集器中
        mylog.addHandler(fl)
        # 设置日志输出格式
        fl.setFormatter(formatted)
        # 返回自定义的日志收集器
        return mylog

do_log = HandleLogs.create_log()
if __name__ == '__main__':
    do_log = HandleLogs.create_log()
    do_log.debug('xixi')
