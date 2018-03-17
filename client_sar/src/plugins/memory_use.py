# -*- coding: utf-8 -*-  
# -*- coding: utf-8 -*-
import os

from lib.config.config import settings


class Memory(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self, command_func, debug):
        if debug:
            output = open(os.path.join(settings.BASEDIR, 'files/memory.out'), 'r', encoding='utf-8').read()
        else:
            output = command_func('sar -r 3 3')

        return self.parse(output,debug)

    def parse(self, content,deug):
        """
        :param content:
        :return:
        """
        memory_list = content.split()
        if deug:
            import random
            memory_avg_num=random.randrange(50,100)
        else:
            memory_avg_num = float(memory_list[-8])
        return {'memory_avg': memory_avg_num}
