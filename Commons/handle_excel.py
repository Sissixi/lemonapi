"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/5 0005上午 7:25
"""
import openpyxl
import os
from Commons.handle_yaml import do_yaml
from Commons.handle_path import DATAS_DIR


class Datas:
    '''存放读取出来的测试用例数据类'''
    pass


class HandleExcel:
    def __init__(self, sheetname, filename=None):
        '''
        初始化设置实例属性-文件名与表单名
        :param filename: 文件名
        :param sheetname: 表单名
        '''
        #如果文件名为空，默认值为路径拼接加配置文件名读取
        if filename is None:
            self.filename = os.path.join(DATAS_DIR, do_yaml.read_yaml('excel', 'excelname'))
        else:
            self.filename = filename
        self.sheetname = sheetname

    def open(self):
        '''封装一个打开方法'''
        # 打开excle文件
        self.wb = openpyxl.load_workbook(self.filename)
        # 选择工作簿中的某个表单
        self.sh = self.wb[self.sheetname]

    def read_excel(self):
        # 先调用打开方法
        self.open()
        # 按行读取表单中的格式对象
        rows = list(self.sh.rows)
        # 创建一个空列表存放读取出的测试用例数据
        cases = []
        # 获取excel表头
        title = [i.value for i in rows[0]]
        # 先按行获取除表头以外的行
        for k in rows[1:]:
            # 再获取每一行的数据内容
            data_value = [j.value for j in k]
            # 创建一个实例对象
            dt = Datas()
            # 将表头与除表头以外的每一行数据，聚合打包，遍历，动态设置类属性，每一行的表头设置为属性名，值设置为属性值
            for c in zip(title, data_value):
                setattr(dt, c[0], c[1])
            cases.append(dt)
        # 关闭excel文件
        self.wb.close()
        # 返回读出的测试用例数据,是对象嵌套列表的格式
        return cases

    def write_excel(self, row, column, value):
        # 打开方法的调用
        self.open()
        # 写入内容
        self.sh.cell(row=row, column=column, value=value)
        # 保存写入的内容
        self.wb.save(self.filename)
        # 关闭
        self.wb.close()


if __name__ == '__main__':
    do_excel = HandleExcel('registers')
    res = do_excel.read_excel()
    print(res)
