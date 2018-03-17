# -*- coding: utf-8 -*-  
import datetime

from backend.service import ssh_interactive
from reposity import models


def token_auth():
    count = 0
    while count < 3:
        user_input = input("Input your access token, press Enter if doesn't have:").strip()
        if len(user_input) == 0:
            return
        if len(user_input) != 8:
            print("token length is 8")
        else:
            time_obj = datetime.datetime.now() - datetime.timedelta(seconds=300)  # 5mins ago
            token_obj = models.Token.objects.filter(val=user_input, date__gt=time_obj).first()
            if token_obj:

                if token_obj.val == user_input:  # 口令对上了
                    user = token_obj.account.user
                    return token_obj, user


def start():
    """启动交互程序"""
    token_obj, user = token_auth()
    if token_obj:
        ssh_interactive.ssh_session(token_obj.host_user_bind, user)
        exit()
