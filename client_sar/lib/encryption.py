# _*_coding:utf-8_*_
# Author:xupan
import hashlib
import time

from Crypto.Cipher import AES
from lib.config.config import settings


def encrypt(data):
    """
    数据加密 ：通过AES数据加密。由于AES数据加密需要16字节的倍数
    因此，在最后加上 len长度的len数据
    :param message:
    :return:
    """
    key = settings.DATA_KEY  # 加密密码
    cipher = AES.new(key, AES.MODE_CBC, key)  # 新建AES加密
    byte_data = bytearray(data, encoding='utf-8')  # 把数据变成bytes
    old_len = len(byte_data)  # 计算长度
    v = old_len % 16  # 取余
    # 在最后增加 长度个数的长度数
    if v == 0:
        back_data = 16
    else:
        back_data = 16 - v
    for i in range(back_data):
        byte_data.append(back_data)
    final_data = byte_data.decode('utf-8')  # 把bytes变成 utf-8
    msg = cipher.encrypt(final_data)  # 加密
    return msg


def auth_check():
    """
    和API验证
    :return:
    """
    ctime = time.time()
    key = settings.APIKEY
    dynamic_key = "{0}|{1}".format(key, ctime)
    m = hashlib.md5()
    m.update(bytes(dynamic_key, encoding='utf-8'))
    md5_key = m.hexdigest()
    md5_dynamic_key = "{0}|{1}".format(md5_key, ctime)

    return md5_dynamic_key
