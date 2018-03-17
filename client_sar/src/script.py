# -*- coding: utf-8 -*-  
from lib.config.config import settings

from .client import Agenttype
from .client import SSHSALTType


def run():
    """
    执行AGENT 或者 SSH SALT 操作 脚本
    :return:
    """
    if settings.MODE == 'AGENT':
        obj = Agenttype()

    else:
        obj = SSHSALTType()
    if settings.DEBUG:
        import time
        print('DEBUG 模式')
        while True:
            obj.execute()
            time.sleep(1)
    obj.execute()