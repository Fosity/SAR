# -*- coding: utf-8 -*-  
import os
import sys

os.environ['USER_SETTINGS'] = 'config.settings'
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from src import script

if __name__ == '__main__':
    script.run()

