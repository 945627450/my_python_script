# my_python_script

## nd-test1.py 说明
#### 参数解释
1. -p/--path 日志文件路径
2. -k/--key 搜索的Key
3. -m 是否对max_list进行排序
4. -d 是否进行绘图
5. -pk 如果进行绘图 那么根据哪个列表进行绘图 接受以下参数
    - count
    - total
    - average
    - max
    - all

#### 函数注解
1. _argparse 脚本参数的配置
2. is_here 日志文件是否存在的判断
3. get_list_sum 获取列表和且输出字符串结果
4. get_list_percent 获取列表的百分比坐标
5. draw_pic 根据单个列表绘图
6. main 主逻辑