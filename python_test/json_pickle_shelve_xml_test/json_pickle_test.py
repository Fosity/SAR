# -*- coding: utf-8 -*-  
import json
import pickle

data={'k1':123,'k2':'hello'}

p_str=pickle.dumps(data)
print(p_str)
p_result=pickle.loads(p_str)
print(p_result,p_result.get('k1'))

j_str=json.dumps(data)
print(j_str)
j_result=json.loads(j_str)
print(j_result,j_result.get('k1'))