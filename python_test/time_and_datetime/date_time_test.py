# -*- coding: utf-8 -*-  
import datetime

d = datetime.datetime.now()
print(d)  # 2018-03-08 17:46:55.157314
print(d.timestamp())  # 1520502415.157314
print(d.today())  # 2018-03-08 17:46:55.157314
print(d.year)  # 2018
print(d.timetuple())
# time.struct_time
# (tm_year=2018, tm_mon=3, tm_mday=8, tm_hour=17, tm_min=46, tm_sec=55, tm_wday=3, tm_yday=67, tm_isdst=-1)

d1=datetime.date.fromtimestamp(322222)
print(d1)   #1970-01-05  把一个时间戳转为datetime日期类型


c=d+datetime.timedelta(4) #加四天
print(c)   #2018-03-12 17:49:11.536833

c1=d+datetime.timedelta(hours=4)  # 加4个小时
print(c1)

e=d.replace(year=2099,month=11,day=20)   #时间替换
print(e)  #2099-11-20 17:51:03.106900
import time
time1='2018-01-01'
abc=time.mktime(time.strptime(time1,"%Y-%m-%d"))
print(abc)