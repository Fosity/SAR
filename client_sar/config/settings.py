# -*- coding: utf-8 -*-  
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER = 'root'
PWD = "123"
# 获取命令模式
MODE = "AGENT"  # SALT   or   SSH
DEBUG = True  # False

#### ssh 登录 ####
SSH_USER = "root"
SSH_PWD = "root"
SSH_KEY = "/xxx/xxx/xx"
SSH_PORT = 22

PLUGINS_DICT = {
    'cpu_use':'src.plugins.cpu_use.Cpu',
    'memory_use':'src.plugins.memory_use.Memory',
}

# 电脑唯一标示
CERT_PATH = os.path.join(BASEDIR, 'config', 'certhostname')

DATA_KEY = b'xxxxxxxxxxxxxxxx'  # AES 需要16位字节 数据加密
APIKEY = "xxxxxxxx"  # API请求验证

API = "http://127.0.0.1:8000/api/asset.html"

HOST_NAME='xxx'