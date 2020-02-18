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


def draw_pre(data, time_list, rtype):
    # 从字典中根据时间提取数据列
    # 根据rtype判断取数据列的第几个索引
    result_list = []
    for ctime in time_list:
        result_list.append(float(data[ctime][rtype]))
    return result_list


def draw_pre_time(data, etype):
    # 时间提取排序等
    # 根据etype判断返回str还是datetime
    temp = data.keys()
    temp.sort()
    if etype == 0:
        return temp
    else:
        return [datetime.strptime(t, '%H:%M:%S') for t in temp]


def main():
    # 设置递归深度
    sys.setrecursionlimit(999999999)

    # 忽略将会被弃用的语义报错
    simplefilter(action='ignore', category=FutureWarning)
    parser = _argparse()

    # 变量定义
    data = {}
    i = 1
    time_temp = ''
    count_sum = 0
    total_sum = 0
    max_temp = []
    option_list = ["count", "total", "average", "max", "all"]

    if parser.draw_switch is True:
        # 判断plot_key是否有值
        if parser.plot_key not in option_list:
            raise SystemExit("绘图参数不正确. 请查看脚本帮助")

    # 文件检测
    is_here(parser.path)

    # 读取文件 清洗文件数据
    with open(parser.path) as f:
        for line in f:
            if re.findall(r'(\d{2}:\d{2}:\d{2})', line) and not bool(re.search('[a-zA-Z]', line)):
                if i % 2 != 0:
                    time_temp = str(re.findall(r'(\d{2}:\d{2}:\d{2})', line)[0])
                    data[time_temp] = {}
                    i += 1
                else:
                    i += 1
                    time_temp = ''
                    continue
            elif re.findall(r'^.*?：', line):
                data[time_temp][str(re.findall(r'^.*?：', line)[0]).split("：")[0]] = [
                    str(re.findall(r'[[](.*?)[]]', line)[0]),
                    str(re.findall(r'[[](.*?)[]]', line)[1]),
                    str(re.findall(r'[[](.*?)[]]', line)[2]),
                    str(re.findall(r'[[](.*?)[]]', line)[3])]

    list_temp = []
    for key in data:
        for key2 in data[key]:
            if parser.key in key2:
                if parser.key != key2:
                    print(parser.key + " 可能为 '" + key2 + "'")
                    raise SystemExit("您输入的key可能不完整，请输入'：'前的完整key。")
                else:
                    list_temp.append(data[key][key2])
                    print(
                        "{0}：count[{1}], total[{2}]ms, average[{3}]ms, max[{4}]ms.\n".format(parser.key,
                                                                                             data[key][key2][0],
                                                                                             data[key][key2][1],
                                                                                             data[key][key2][2],
                                                                                             data[key][key2][3]))
    print("一共匹配到：{}次. \n".format(len(list_temp)))

    print("以下为统计结果=======================================================")

    try:
        # 数据统计
        for i in list_temp:
            count_sum += int(i[0])
            total_sum += int(i[1])
            max_temp.append(i[3])

        avg_result = str(round(float(total_sum) / float(count_sum), 2))

        count_sum = str(count_sum)
        total_sum = str(total_sum)

        print(parser.key + " count[{0}], total[{1}]ms, average[{2}]ms, max[{3}]ms. \n".format(count_sum, total_sum,
                                                                                              avg_result,
                                                                                              str(max(max_temp))))
    except ZeroDivisionError:
        # 除数不能为零
        print("ZeroDivisionError average is null...")
        print(
            parser.key + " count[{0}], total[{1}]ms, max[{2}]ms. \n".format(count_sum, total_sum,
                                                                            str(max(max_temp))))

    if parser.boolean_switch is True:
        # 是否进行max列升序排列的开关
        print("以下为max升序排列结果================================================")
        max_temp.sort(reverse=False)

        print("0%   = {},\n1%   = {},\n50%  = {},\n90%  = {},\n99%  = {},\n100% = {}".format(max_temp[1], max_temp[
            get_list_percent(max_temp, 0.01)], max_temp[get_list_percent(max_temp, 0.50)], max_temp[
                                                                                                 get_list_percent(
                                                                                                     max_temp,
                                                                                                     0.90)],
                                                                                             max_temp[
                                                                                                 get_list_percent(
                                                                                                     max_temp,
                                                                                                     0.99)],
                                                                                             max_temp[-1]))

    if parser.draw_switch is True:
        print("\n绘图数据处理中======================================================")
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

        plot_data = {}
        for i in data:
            try:
                plot_data[i] = data[i][parser.key]
            except KeyError:
                print("\n================================================")
                print(str(i) + " 补数据")
                # 缺数据用0补上
                data[i][parser.key] = [0, 0, 0, 0]
                plot_data[i] = data[i][parser.key]

        # 时间处理
        time_list = draw_pre_time(plot_data, 0)
        time_temp = draw_pre_time(plot_data, 1)

        print("\n请耐心等待正在绘图==================================================")
        if parser.plot_key == 'count':
            draw_pic(fig1, draw_pre(plot_data, time_list, 0), time_temp)
        elif parser.plot_key == 'total':
            draw_pic(fig1, draw_pre(plot_data, time_list, 1), time_temp)
        elif parser.plot_key == 'average':
            draw_pic(fig1, draw_pre(plot_data, time_list, 2), time_temp)
        elif parser.plot_key == 'max':
            draw_pic(fig1, draw_pre(plot_data, time_list, 3), time_temp)
        elif parser.plot_key == 'all':
            # 画图
            plt.plot(time_temp, draw_pre(plot_data, time_list, 0), '--', c='b', label='count')
            plt.plot(time_temp, draw_pre(plot_data, time_list, 1), '--', c='red', label='total')
            plt.plot(time_temp, draw_pre(plot_data, time_list, 2), '--', c='g', label='average')
            plt.plot(time_temp, draw_pre(plot_data, time_list, 3), '--', c='k', label='max')

            # 时间自动格式化
            plt.gcf().autofmt_xdate()

            # 开启图例
            plt.legend()
            plt.show()

        else:
            raise SystemExit("绘图参数不正确. 请联系作者")


if __name__ == '__main__':
    main()
