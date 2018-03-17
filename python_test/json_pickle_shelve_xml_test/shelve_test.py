# -*- coding: utf-8 -*-  
"""
 shelve模块 是一个简单的k，v 将内存数据通过文件持久化的模块，可以持久化任何pikcle 可支持的Python数据格式
"""
import shelve

f=shelve.open('shelve_test')

name=['aaa','bbb','vvv']
f['name']=name

f.close()
################################
import shelve
d=shelve.open('shelve_test')

print(d['name'])
