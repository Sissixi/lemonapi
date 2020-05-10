"""
-*-coding:utf-8 -*-
Author:xixi
Time:2020/5/5 0005上午 7:25
"""
import yaml
from Commons.handle_path import CONFIG_FILE_PATH


class HandleYaml:
    def __init__(self, filename):
        with open(filename, encoding='utf8')as one_file:
            self.datas = yaml.full_load(one_file)

    def read_yaml(self, section, option):
        return self.datas[section][option]

    @staticmethod
    def write_yaml(filename, data):
        with open(filename, 'w', encoding='utf8') as two_file:
            yaml.dump(data, two_file, allow_unicode=True)


do_yaml = HandleYaml(CONFIG_FILE_PATH)
if __name__ == '__main__':
    do_yaml = HandleYaml(CONFIG_FILE_PATH)
    data={"xixi":{"haha":1}}
    do_yaml.write_yaml('excel.yaml', data)
