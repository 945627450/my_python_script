# -*- coding: utf-8 -*-
# @Time    : 2020-02-20 20:31
# @Author  : Embiid.Huang
# @Email   : hzx945627450@163.com
# @File    : deal_md5.py
# @Software: PyCharm

from __future__ import print_function

import re
import os
import argparse


def _argparse():
    # 脚本参数配置
    parser = argparse.ArgumentParser(description='md5 check result deal script')
    # 读取的文件路径
    parser.add_argument('-p', '--path', action='store', dest='path',
                        required=True, help='txt path')
    return parser.parse_args()


def is_here(file_path):
    # 判断文件路径是否正确及是否可读
    if not os.path.isfile(file_path):
        raise SystemExit(file_path + " 路径错误，或者没有该文件，请检查.")
    elif not os.access(file_path, os.R_OK):
        raise SystemExit("很抱歉您没有读取权限.")
    else:
        pass


def main():
    parser = _argparse()
    with open(parser.path) as f:
        for line in f:
            if "\\" in line:
                print("文件名:" + line.split("\\")[-1].replace('\n', '').replace('\r', ''))
            elif re.search('^[a-fA-F0-9]{32}$', line):
                print("MD5:" + line, end='')
                # print("MD5:" + line)


if __name__ == '__main__':
    main()
