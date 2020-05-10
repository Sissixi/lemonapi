"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/6 0006下午 9:21
"""
import re
from Commons.handle_mysql import HandleMysql
from Commons.handle_yaml import HandleYaml
from Commons.handle_path import USER_DATA


class Parameterization:
    '''
    参数化类
    '''
    # 注册接口--不存在的手机号码
    not_existed_tel_pattern = r'{not_existed_tel}'
    # 登录接口--存在的手机号码，投资人的手机号码
    exist_tel_pattern = r'{invest_user_tel}'
    # 获取用户信息读取类
    user_yaml = HandleYaml(USER_DATA)
    # 充值接口--投资人用户id
    recharge_id = r'{invest_user_id}'
    # 充值接口--不存在的用户id
    not_id = r'{invest_not_user_id}'

    # 加标接口--借款人id
    borrow_id = r'{borrow_user_id}'
    # 加标接口--借款人手机号码
    borrow_tel = r'{borrow_user_tel}'

    # 投资接口--管理员手机号码
    admin_tel = r'{admin_user_tel}'
    # 投资接口--标id
    load_id_pattern = r'{loan_id}'
    # 标id不存在
    loan_not_id = r'{loan_not_id}'

    @classmethod
    def not_exist_param(cls, data):
        # 创建mysql对象
        do_mysql = HandleMysql()
        # 如果有待匹配的数据，返回search对象后再去使用sub替换
        if cls.not_existed_tel_pattern in data:
            '''注册接口--不存在的手机号码'''
            # 调用mysql创建随机的数据
            mobile = do_mysql.not_exist_mobile()
            # 使用sub替换
            data = re.sub(cls.not_existed_tel_pattern, mobile, data)
        if re.search(cls.not_id, data):
            '''充值接口--不存在的用户id'''
            sql = 'SELECT id FROM member ORDER BY id DESC LIMIT 0,1;'
            max_sql = str(do_mysql.run(sql)['id'] + 1)
            data = re.sub(cls.not_id, max_sql, data)
        if re.search(cls.loan_not_id, data):
            '''充值接口--不存在的标id'''
            sql = 'SELECT id FROM invest ORDER BY id desc LIMIT 0,1;'
            max_sql = str(do_mysql.run(sql)['id'] + 1)
            data = re.sub(cls.loan_not_id, max_sql, data)
        # 关闭mysql
        do_mysql.close()
        return data

    @classmethod
    def invest_data(cls, data):
        if re.search(cls.admin_tel, data):
            '''投资接口--管理人手机号码'''
            # 获取借款人手机号码
            admin_user_tel = str(cls.user_yaml.read_yaml('admin', 'mobile_phone'))
            data = re.sub(cls.admin_tel, admin_user_tel, data)
        if re.search(cls.load_id_pattern, data):
            '''投资接口--load_id'''
            # 获取load_id
            load_id = str(getattr(cls, "load_id"))
            data = re.sub(cls.load_id_pattern, load_id, data)
        return data

    @classmethod
    def add_data(cls, data):
        if re.search(cls.borrow_id, data):
            '''加标接口--借款人id'''
            # 获取借款人id
            borrow_user_id = str(cls.user_yaml.read_yaml('borrow', 'id'))
            data = re.sub(cls.borrow_id, borrow_user_id, data)
        if re.search(cls.borrow_tel, data):
            '''加标接口--借款人手机号码'''
            # 获取借款人手机号码
            borrow_user_tel = str(cls.user_yaml.read_yaml('borrow', 'mobile_phone'))
            data = re.sub(cls.borrow_tel, borrow_user_tel, data)
        return data

    @classmethod
    def other_data(cls, data):
        if re.search(cls.exist_tel_pattern, data):
            '''登录接口--存在的手机号码，投资人的手机号码;投资人手机号码替换'''
            invest_mobile = cls.user_yaml.read_yaml('invest', 'mobile_phone')
            data = re.sub(cls.exist_tel_pattern, invest_mobile, data)
        if re.search(cls.recharge_id, data):
            '''充值接口--投资用户id'''
            invest_user_id = str(cls.user_yaml.read_yaml('invest', 'id'))
            data = re.sub(cls.recharge_id, invest_user_id, data)
        return data

    @classmethod
    def to_param(cls, data):
        data = cls.not_exist_param(data)
        data = cls.other_data(data)
        data = cls.add_data(data)
        data = cls.invest_data(data)
        # 返回替换后的数据
        return data


if __name__ == '__main__':
    str1 = '{"member_id":{invest_user_id},"loan_id":{loan_not_id},"amount":5000}'
    data = Parameterization.to_param(str1)
    print(data, type(data))
