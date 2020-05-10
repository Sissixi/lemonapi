"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/7 0007下午 8:57
"""
from Commons.handle_requests import HandleRequests
from Commons.handle_mysql import HandleMysql
from Commons.handle_yaml import do_yaml
from Commons.handle_path import USER_DATA


def create_new_user(reg_name, pwd='12345678', type=1):
    '''
    创建一个用户信息
    :param reg_name:用户名
    :param pwd:密码
    :param type:类型
    :return:用户信息，嵌套字典的字典，用户名是key，用户信息是value
    '''
    # 建立连接
    do_mysql = HandleMysql()
    # 建立会话
    do_request = HandleRequests()
    # 添加公共请求头
    do_request.add_headers(do_yaml.read_yaml("api", "version"))
    # 获取url
    url = do_yaml.read_yaml("api", "base_url") + "/member/register"
    # 获取注册成功的id
    sql_id = do_yaml.read_yaml("mysql", "sql2")
    while True:
        # 获取一个不存在的手机号码
        mobile_phone = do_mysql.not_exist_mobile()
        # 请求参数data
        data = {
            "mobile_phone": mobile_phone,
            "pwd": pwd,
            "type": type,
            "reg_name": reg_name
        }
        # 向服务器发起请求
        do_request.send(url=url, data=data)
        # 获取用户id,字典类型
        user_id = do_mysql.run(sql_id, args=[mobile_phone])
        #如果有用户id，取出用户id
        if user_id:
            id = user_id['id']
            break
        # 用户信息
    user_dict = {
        reg_name: {
            "reg_name": reg_name,
            "id": id,
            "pwd": pwd,
            "mobile_phone": mobile_phone
        }
    }
    # 关闭连接
    do_mysql.close()
    # 关闭会话
    do_request.close()


    return user_dict


def new_data():
    new_dict = {}
    new_dict.update(create_new_user('admin', type=0))
    new_dict.update(create_new_user('invest'))
    new_dict.update(create_new_user('borrow'))
    do_yaml.write_yaml(data=new_dict, filename=USER_DATA)


if __name__ == '__main__':
    new_data()
