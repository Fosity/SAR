# -*- coding: utf-8 -*-  
import logging
class IgnoreBackupLogFilter(logging.Filter):
    """忽略带db backup 的日志"""
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

# 调用logger
logger.debug("test ....")
logger.info("test info ....")
logger.warning("start to run db backup job ....")
logger.error("test error ....")