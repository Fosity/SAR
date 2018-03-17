# -*- coding: utf-8 -*-  
import importlib
import paramiko
import subprocess
import traceback
from lib.config.config import settings


class PluginManager(object):

    def __init__(self,hostname=None):
        self.hostname=hostname
        self.plugin_dict = settings.PLUGINS_DICT
        self.debug = settings.DEBUG  # if True  则程序在debug调试过程
        self.mode = settings.MODE
        if self.mode == "SSH":
            self.ssh_user = settings.SSH_USER
            self.ssh_port = settings.SSH_PORT
            self.ssh_pwd = settings.SSH_PWD
            self.ssh_key = settings.SSH_KEY

    def exec_plugin(self):
        response={}
        for k,v in self.plugin_dict.items():
            ret={'status':True,'data':None}
            try:
                module_path,class_name=v.rsplit('.',1)
                module_import=importlib.import_module(module_path)
                cls_obj=getattr(module_import,class_name)
                if hasattr(cls_obj,'initial'):
                    obj=cls_obj.initial()
                else:
                    obj=cls_obj()
                result=obj.process(self.command,self.debug)
                ret['data']=result
            except Exception as e:
                ret['status']=False
                ret['data']= "[{0}][{1}]采集数据出现错误：{2}".format(self.hostname if self.hostname else "AGENT", k,
                                                              traceback.format_exc())

            response[k]=ret
        return response


    def command(self,cmd):
        if self.mode == "AGENT":
            return self.__agent(cmd)
        elif self.mode == "SSH":
            return self.__salt(cmd)
        elif self.mode == "SALT":
            return self.__ssh(cmd)
        else:
            raise Exception('模式错误，只能是AGENT,SSH,SALT')

    def __agent(self, cmd):
        """
        AGENT 模式下执行
        :param cmd:
        :return:
        """
        output = subprocess.getoutput(cmd)
        return output

    def __salt(self, cmd):
        """
        对于py2.x 调用 salt.client.LocalClient()
        对于py3.x 则使用 "salt '%s' cmd.run '%S' " %(hostname,cmd)
        :param cmd:
        :return:
        """
        # 对于py2.x
        # import salt.client
        # local = salt.client.LocalClient()
        # result = local.cmd(self.hostname, 'cmd.run', [cmd])
        # return result[self.hostname]
        salt_cmd = "salt '{0}' cmd.run '{1}".format(self.hostname, cmd)
        output = subprocess.getoutput(salt_cmd)
        return output

    def __ssh(self, cmd):
        """

        :param cmd:
        :return:
        """
        private_key = None
        if self.ssh_key:
            private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd,
                    pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result