# _*_coding:utf-8_*_
# Author:xupan
import hashlib
import time

from Crypto.Cipher import AES
from django.conf import settings


def decryption(request, api_key_record):
	client_md5_time_key = request.META.get('HTTP_OPENKEY')
	client_md5_key, client_ctime = client_md5_time_key.split('|')
	client_ctime = float(client_ctime)
	server_time = time.time()

	if server_time - client_ctime > 10:
		return False

	key = settings.AUTH_KEY
	server_dynamic_key = "{0}|{1}".format(key, client_ctime)
	m = hashlib.md5()
	m.update(bytes(server_dynamic_key, encoding='utf-8'))
	server_md5_key = m.hexdigest()
	if server_md5_key != client_md5_key:
		return False

	for key in list(api_key_record.keys()):
		v = api_key_record[key]
		if server_time > v:
			del api_key_record[key]

	if client_md5_time_key in api_key_record:
		return False
	else:
		api_key_record[client_md5_time_key] = client_ctime + 10
	return True


def decrypt(msg):
	"""
	数据解密
	:param tz:
	:return:
	"""
	key = settings.DATA_KEY
	cipher = AES.new(key, AES.MODE_CBC, key)
	result = cipher.decrypt(msg)
	data = result[0:-result[-1]]
	return str(data, encoding='utf-8')
