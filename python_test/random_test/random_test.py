# -*- coding: utf-8 -*-  
import random

a=random.randrange(1,10)  #返回1-10之间的一个随机数，不包括10
print(a)

b=random.randint(1,10)  #返回1-10之间的一个随机数，包括10
print(b)

c=random.randrange(0, 100, 2) #随机选取0到100间的偶数
print(c)

d=random.random()   #返回一个随机浮点数
print(d)

e= random.choice('abce3#$@1') #返回一个给定数据集合中的随机字符
print(e)

f=random.sample('abcdefghij',3)  #从多个字符中选取特定数量的字符
print(f)  #['f', 'i', 'g']

import string
#生成随机字符串
g=''.join(random.sample(string.ascii_lowercase+string.digits,6))
print(g)

#洗牌
h=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
random.shuffle(h)
print(h)