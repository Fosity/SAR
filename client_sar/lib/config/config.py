# -*- coding: utf-8 -*-  
import importlib
import os

from . import global_settings

class Settings(object):
    def __init__(self):
        # 从默认配置中找到配置 并执行 self.name=value
        for name in dir(global_settings):
            if name.isupper():
                value = getattr(global_settings, name)
                setattr(self, name, value)

        # 从系统全局变量中找到，用户定义配置的路径 environ[USER_SETTINGS]="config.settings"
        user_settings_path = os.environ.get('USER_SETTINGS')

        if not user_settings_path:
            return
        # 导入用户自定义配置文件。
        new_settings = importlib.import_module(user_settings_path)

        # 从用户自定义配置文件找到配置，并替换默认配置（自动），执行配置
        for name in dir(new_settings):
            if name.isupper():
                value = getattr(new_settings, name)
                setattr(self, name, value)


# 配置初始化
settings = Settings()