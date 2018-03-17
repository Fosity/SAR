# -*- coding: utf-8 -*-  
import os
import re
from lib.config.config import settings

class Cpu(object):
    def __init__(self):
        pass
    @classmethod
    def initial(cls):
        return cls()


    def process(self,command_func,debug):
        if debug:
            output=open(os.path.join(settings.BASEDIR, 'files/cpu.out'), 'r', encoding='utf-8').read()
        else:
            output=command_func('sar -P ALL 3 3')

        return self.parse(output,debug)

    def parse(self,content,debug):
        """
        :param content:
        :return:
        """
        cpu_num = int(re.compile('(\d+) CPU').findall(content)[0])
        cpu_list = content.split()
        cpu_list1 = cpu_list[7:]
        cpu_dict = {}
        for i in range(cpu_num):
            cpu_dict[str(i)] = {}
            cpu_dict[str(i)]['all'] = cpu_list1[15 + i * 32]
            index = 15 + i * 32
            for j in range(cpu_num):
                cpu_dict[str(i)][str(j)] = cpu_list1[index + (j + 1) * 8]
        cpu_avg_dict = {}
        for k1, v1 in cpu_dict['0'].items():
            cpu_avg_dict[k1] = 0
        for k, v in cpu_dict.items():
            for k1, v1 in v.items():
                cpu_avg_dict[k1] += float(v1)
        if debug:
            import random
            for k, v in cpu_avg_dict.items():
                cpu_avg_dict[k] = random.randrange(80,100)
        else:
            for k, v in cpu_avg_dict.items():
                cpu_avg_dict[k] = v / cpu_num
        return  cpu_avg_dict