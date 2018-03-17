# -*- coding: utf-8 -*-  
import json
import os
import requests
from lib.config.config import settings
from lib.encryption import encrypt, auth_check
from src.plugins import PluginManager


class Base(object):
    def post_asset(self, result_info):
        data = encrypt(json.dumps(result_info))
        requests.post(
            url=settings.API,
            data=data,
            headers={'Content-Type': 'application/json', 'OpenKey': auth_check()}
        )

class Agenttype(Base):
    def execute(self):
        """
        """
        result_info = PluginManager().exec_plugin()
        result_info['hostname']=open(os.path.join(settings.BASEDIR, 'config/certhostname'), 'r', encoding='utf-8').read()
        print(result_info)
        self.post_asset(result_info)


class SSHSALTType(Base):
    def execute(self):
        """
        """
        result_info = PluginManager(settings.HOST_NAME).exec_plugin()
        self.post_asset(result_info)