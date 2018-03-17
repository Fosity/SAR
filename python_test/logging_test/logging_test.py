# -*- coding: utf-8 -*-  
""""""
"""
很多程序都有记录日志的需求，并且日志中包含的信息 有正常的程序访问日志，还有 错误、警告灯信息输出。
python 的logging模块提供了标准的日志借口。
logging的日志分为
debug(),info(),warning(),error(),critical() 5个等级

DEBUG: Detailed information,typically or interest only when diagnosing problems
INFO : Confirmation that things are working as expected
WARNING: An indication that something unexpected happened,or indicative of some problem
        in the near future .The software is still working as expected
ERROR: Due to a more serious problem, the software has not been able to perform some function
CRITICAL: A serious error, indicating that the program itself may be unable to continue running

"""
import logging

logging.basicConfig(filename='example.log', level=logging.INFO)
logging.debug('This message should go to ')
logging.info('So should this')
logging.warning('And this ,too')

"""自定义日志格式"""
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')
"""
除了加时间，还可以自定义一大堆格式，下表就是所有支持的格式
%(name)s    Logger的名字
%(levelno)s	    数字形式的日志级别
%(levelname)s	文本形式的日志级别
%(pathname)s	调用日志输出函数的模块的完整路径名，可能没有
%(filename)s	调用日志输出函数的模块的文件名
%(module)s	    调用日志输出函数的模块名
%(funcName)s	调用日志输出函数的函数名
%(lineno)d	    调用日志输出函数的语句所在的代码行
%(created)f	    当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d	输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s	    字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d	    线程ID。可能没有
%(threadName)s	线程名。可能没有
%(process)d	    进程ID。可能没有
%(message)s	    用户输出的消息
"""
"""
聊天工具的图形界面模块可以这样获得它的Logger：
LOG=logging.getLogger(”chat.gui”)
而核心模块可以这样：
LOG=logging.getLogger(”chat.kernel”)
还可以绑定handler和filters
Logger.setLevel(lel):指定最低的日志级别，低于lel的级别将被忽略。debug是最低的内置级别，critical为最高
Logger.addFilter(filt)、Logger.removeFilter(filt):添加或删除指定的filter
Logger.addHandler(hdlr)、Logger.removeHandler(hdlr)：增加或删除指定的handler

每个Logger可以附加多个Handler。接下来我们就来介绍一些常用的Handler：
1.logging.StreamHandler 使用这个Handler可以向类似与sys.stdout或者sys.stderr的任何文件对象(file object)输出信息。
2.logging.FileHandler 和StreamHandler 类似，用于向一个文件输出日志信息。不过FileHandler会帮你打开这个文件
3.logging.handlers.RotatingFileHandler
4.logging.handlers.TimedRotatingFileHandler

formatter 组件
日志的formatter是个独立的组件，可以跟handler组合
fh = logging.FileHandler("access.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter) #把formmater绑定到fh上

filter 组件
如果你想对日志内容进行过滤，就可自定义一个filter
class IgnoreBackupLogFilter(logging.Filter):
    # 忽略带db backup 的日志#
    def filter(self, record): #固定写法
        return   "db backup" not in record.getMessage()
        
然后把这个filter添加到logger中
logger.addFilter(IgnoreBackupLogFilter())
"""

"""
一个同时输出到屏幕、文件、带filter的完成例子
import logging
class IgnoreBackupLogFilter(logging.Filter):
    忽略带db backup 的日志
    def filter(self, record): #固定写法
        return   "db backup" not in record.getMessage()

#console handler # 屏幕输出
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

#file handler #文件输出
fh = logging.FileHandler('mysql.log')
#fh.setLevel(logging.WARNING)

#formatter #文件输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#bind formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger = logging.getLogger("Mysql") #实例化
logger.setLevel(logging.DEBUG) #logger 优先级高于其它输出途径的

#add handler   to logger instance
logger.addHandler(ch)
logger.addHandler(fh)

#add filter
logger.addFilter(IgnoreBackupLogFilter())

logger.debug("test ....")
logger.info("test info ....")
logger.warning("start to run db backup job ....")
logger.error("test error ....")
"""
