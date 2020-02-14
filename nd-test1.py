# -*- coding: utf-8 -*-
# @Time    : 2020-02-12 23:00
# @Author  : Embiid.Huang
# @Email   : hzx945627450@163.com
# @File    : nd-test1.py
# @Software: PyCharm


import re
import sys
import argparse

from warnings import simplefilter


def _argparse():
    # 脚本参数配置
    parser = argparse.ArgumentParser(description='A Log Processor')
    # 读取的文件路径
    parser.add_argument('-p', '--path', action='store', dest='path',
                        required=True, help='log path')
    # 查询用key
    parser.add_argument('-k', '--key', action='store', dest='key',
                        required=True, help='match key')
    # 是否对max进行排序
    parser.add_argument('-m', action='store_true', default=False, dest='boolean_switch', help='sort max_list and print')
    return parser.parse_args()


def get_list_sum(list_name, size, w=1):
    # 求和
    if size == 0:
        if w == 1:
            return '0'
        else:
            return 0
    else:
        if w == 1:
            return str(float(list_name[size - 1]) + float(get_list_sum(list_name, size - 1)))
        else:
            return float(list_name[size - 1]) + float(get_list_sum(list_name, size - 1))


def get_list_percent(list_name, percent_num):
    # 求百分比位置下标
    m_length = len(list_name)
    m = int(round(m_length * percent_num, 0))
    # 测试代码
    # print(str(percent_num) + "下标为:" + str(m))
    return m


def main():
    # 设置递归深度
    sys.setrecursionlimit(999999999)

    # 忽略将会被弃用的语义报错
    simplefilter(action='ignore', category=FutureWarning)
    parser = _argparse()

    # 定义变量
    count_list = []
    total_list = []
    average_list = []
    max_list = []
    hit_number = 0

    with open(parser.path) as f:
        print("以下是检索结果=======================================================")
        for line in f:
            if line.find(parser.key) == 0:
                count_list.append(re.findall(r'[[](.*?)[]]', line)[0])
                total_list.append(re.findall(r'[[](.*?)[]]', line)[1])
                average_list.append(re.findall(r'[[](.*?)[]]', line)[2])
                max_list.append(re.findall(r'[[](.*?)[]]', line)[3])
                print(line)
                hit_number += 1
            else:
                continue

    if hit_number == 0:
        print("未匹配到包含" + key + "的行...")
        exit(9999)

    print("一共匹配到：{}次. \n".format(hit_number))

    print("以下为统计结果=======================================================")

    print(
        parser.key + " count[{0}], total[{1}]ms, average[{2}]ms, max[{3}]ms. \n".format(
            get_list_sum(count_list, len(count_list)),
            get_list_sum(total_list, len(total_list)),
            str(round(get_list_sum(
                total_list, len(total_list),
                0) / get_list_sum(count_list,
                                  len(count_list), 0),
                      2)),
            str(max(max_list))))

    if parser.boolean_switch is True:
        print("以下为max升序排列结果================================================")
        max_list.sort(reverse=False)

        # 测试代码
        # print(max_list, len(max_list), max_list[1], max_list[get_list_percent(max_list, 0.01)],
        #       max_list[get_list_percent(max_list, 0.50)], max_list[get_list_percent(max_list, 0.90)],
        #       max_list[get_list_percent(max_list, 0.99)], max_list[-1])

        print("0%   = {},\n1%   = {},\n50%  = {},\n90%  = {},\n99%  = {},\n100% = {}".format(max_list[1], max_list[
            get_list_percent(max_list, 0.01)], max_list[get_list_percent(max_list, 0.50)], max_list[
                                                                                                 get_list_percent(
                                                                                                     max_list,
                                                                                                     0.90)],
                                                                                             max_list[
                                                                                                 get_list_percent(
                                                                                                     max_list,
                                                                                                     0.99)],
                                                                                             max_list[-1]))


if __name__ == '__main__':
    main()
