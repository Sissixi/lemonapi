"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/5 0005上午 7:26
"""
import pymysql
import random
from Commons.handle_yaml import do_yaml


class HandleMysql:
    def __init__(self):
        # 建立连接对象
        self.conn = pymysql.connect(host=do_yaml.read_yaml('mysql', 'host'),
                                    user=do_yaml.read_yaml('mysql', 'user'),
                                    password=do_yaml.read_yaml('mysql', 'password'),
                                    database=do_yaml.read_yaml('mysql', 'database'),
                                    port=3306,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        # 通过连接对象建立游标对象
        self.cursor = self.conn.cursor()

    def run(self, sql, args=None, is_more=False):
        '''
        执行sql
        :param sql:要执行的sql语句
        :param args:sql语句中要传递的参数，不传参数默认为none
        :param is_more:is_more默认为False，获取一条结果
        :return:
        '''
        # 通过游标对象执行sql
        self.cursor.execute(sql, args)
        # 通过连接对象提交
        self.conn.commit()
        # 如果为true，获取一条全部结果
        if is_more:
            return self.cursor.fetchall()
        # 否则，获取一条全部结果
        else:
            return self.cursor.fetchone()

    def close(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()

    @staticmethod
    def mobile_phone():
        '''随机生成11位手机号码'''
        return "188" + "".join(random.sample('0123456789', 8))

    def not_phone(self, mobile):
        '''判断手机号码是否存在'''
        sql = do_yaml.read_yaml('mysql', 'sql1')
        # 手机号码存在返回true
        if self.run(sql, args=[mobile]):
            return True
        # 手机号码不存在返回False
        else:
            return False

    def not_exist_mobile(self):
        '''随机生成一个数据库中不存在的手机号码'''
        while True:
            # 生成一个随机的手机号码
            mobile_one = self.mobile_phone()
            # 如果手机号码不存在，返回False，not false为true
            if not self.not_phone(mobile_one):
                break
        # 循环结束，返回数据库中不存在的手机号码mobile_one
        return mobile_one
if __name__ == '__main__':
    print(HandleMysql().not_exist_mobile())