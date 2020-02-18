# -*- coding: utf-8 -*-
# @Time    : 2020-02-12 23:00
# @Author  : Embiid.Huang
# @Email   : hzx945627450@163.com
# @File    : analyzer.py
# @Software: PyCharm


import re
import os
import sys
import argparse

from warnings import simplefilter
from matplotlib import pyplot as plt
from matplotlib import dates as m_date
from datetime import datetime


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

    # 是否需要趋势图
    parser.add_argument('-d', action='store_true', default=False, dest='draw_switch',
                        help='plot someone_list to screen')

    # 趋势图的依据列
    parser.add_argument('-pk', action='store', dest='plot_key',
                        help='assign the list to be plotted, key in ["count", "total", "average", "max", "all"]')

    return parser.parse_args()


def is_here(file_path):
    # 判断文件路径是否正确及是否可读
    if not os.path.isfile(file_path):
        raise SystemExit(file_path + " 路径错误，或者没有该文件，请检查.")
    elif not os.access(file_path, os.R_OK):
        raise SystemExit("很抱歉您没有读取权限.")
    else:
        pass


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
    return m


def draw_pic(fig, list_name, other_list):
    # 绘图
    # y轴 str -> int
    y = [float(item) for item in list_name]

    # 绘制图形
    plt.plot(other_list, y, 'g--', c='orangered')
    plt.gcf().autofmt_xdate()

    # 展示
    plt.show()

    # 保存图片
    fig.savefig('chart.eps', dpi=1200, format='eps', bbox_inches='tight')


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
    time_list = []
    option_list = ["count", "total", "average", "max", "all"]
    hit_number = 0

    if parser.draw_switch is True:
        # 判断plot_key是否有值
        if parser.plot_key not in option_list:
            raise SystemExit("绘图参数不正确. 请查看脚本帮助")

    is_here(parser.path)
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
                # 取时间
                if re.findall(r'(\d{2}:\d{2}:\d{2})', line) and not bool(re.search('[a-zA-Z]', line)):
                    time_list.append(str(re.findall(r'(\d{2}:\d{2}:\d{2})', line)[0]))

    if hit_number == 0:
        raise SystemExit("没有匹配到与 " + parser.key + " 相关的行.")

    print("一共匹配到：{}次. \n".format(hit_number))

    print("以下为统计结果=======================================================")

    try:
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
    except ZeroDivisionError:
        print("ZeroDivisionError average is null")
        print(
            parser.key + " count[{0}], total[{1}]ms, max[{2}]ms. \n".format(
                get_list_sum(count_list, len(count_list)),
                get_list_sum(total_list, len(total_list)),
                str(max(max_list))))

    if parser.boolean_switch is True:
        print("以下为max升序排列结果================================================")
        max_list.sort(reverse=False)

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

    if parser.draw_switch is True:
        # 判断绘图开关是否开启
        # 初始化绘图板
        fig1 = plt.figure(figsize=(30, 5))
        ax1 = fig1.add_subplot(1, 1, 1)
        ax1.xaxis.set_major_formatter(m_date.DateFormatter('%H:%M:%S'))  # 设置时间标签显示格式
        ax1.xaxis.set_major_locator(m_date.MinuteLocator(interval=30))

        # 标签配置
        plt.title("List Trend Chart")
        plt.xlabel('Time')  # x轴标注
        plt.ylabel('Number')  # y轴标注

        # 时间列表的初始化
        # 抛弃多余时间
        time_list = time_list[::2]
        # 格式化时间
        time_list = [datetime.strptime(t, '%H:%M:%S') for t in time_list]

        #  ["count", "total", "average", "max"]
        print("\n请耐心等待正在绘图================================================")
        if parser.plot_key == 'count':
            draw_pic(fig1, count_list, time_list)
        elif parser.plot_key == 'total':
            draw_pic(fig1, total_list, time_list)
        elif parser.plot_key == 'average':
            draw_pic(fig1, average_list, time_list)
        elif parser.plot_key == 'max':
            draw_pic(fig1, max_list, time_list)
        elif parser.plot_key == 'all':
            count_list = [float(item) for item in count_list]
            total_list = [float(item) for item in total_list]
            average_list = [float(item) for item in average_list]
            max_list = [float(item) for item in max_list]
            plt.plot(time_list, count_list, '--', c='b', label='count')
            plt.plot(time_list, total_list, '--', c='red', label='total')
            plt.plot(time_list, average_list, '--', c='g', label='average')
            plt.plot(time_list, max_list, '--', c='k', label='max')
            # 时间自动格式化
            plt.gcf().autofmt_xdate()
            # 开启图例
            plt.legend()
            plt.show()
        else:
            raise SystemExit("绘图参数不正确. 请联系作者")


if __name__ == '__main__':
    main()
