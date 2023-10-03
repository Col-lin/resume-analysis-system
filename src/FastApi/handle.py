import info
import re
import numpy as np
import predict
from collections import OrderedDict
import utils

def re_basedata(basic_data, data):
    if basic_data['tel'] == '':
        tel = re.findall(info.tel_pattern(), data)
        if tel:
            basic_data['tel'] = tel[0]
    if basic_data['email'] == '':
        email = re.findall(info.email_pattern(), data)
        if email:
            basic_data['email'] = email[0]
    if basic_data['age'] == 0:
        age = re.search(info.age_pattern(), data)
        if age:
            if age.group(1):
                basic_data['age'] = int(age.group(1))
            else:
                basic_data['age'] = int(age.group(2))
    if basic_data['birth'] == '':
        birth = re.search(info.birth_pattern(), data)
        if birth:
            basic_data['birth'] = birth.group()
            basic_data['age'] = 2023 - int(basic_data['birth'][:4])+1
    edu = re.findall(info.edu_pattern(), data)
    if edu:
        for e in edu:
            # 找到的学历大于当前的学历就更新
            if info.edu_map()[e] > info.edu_map()[basic_data['edu']]:
                basic_data['edu'] = e
    return basic_data