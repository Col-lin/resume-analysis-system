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

def handle_basedata(data, basic_data, total_data, tokenizer3, model3):
    for data in data[0]:
        # 先跑NER 选出姓名 地点 学历
        output_prediction = predict.ner_predict(
            data, tokenizer3, model3)
        if len(output_prediction[0]) and basic_data['name'] == '' and re.match(info.chinese_str(), output_prediction[0][0]):
            basic_data['name'] = output_prediction[0][0]
        elif len(output_prediction[1]):
            basic_data['college'].extend(output_prediction[1])
        elif len(output_prediction[2]):
            basic_data['loc'].extend(output_prediction[2])
        # 再跑正则匹配更新label
        basic_data = re_basedata(basic_data, data)

    fixed_college = []
    for x in basic_data['college']:
        for keyword in info.college_endword():
            keyword_position = x.find(keyword)
            if keyword_position != -1:
                fixed_college.append(x[:keyword_position + len(keyword)])
                # 注意这里内循环需要是 keyword 并且必须 break 防止识别两次 优先级见 info
                break
    basic_data['college'] = list(OrderedDict.fromkeys(fixed_college))
    basic_data['loc'] = list(OrderedDict.fromkeys(basic_data['loc']))[:2]

    # 给学校加tag
    if np.intersect1d(basic_data['college'], info.college985()).size > 0:
        total_data['tag']['edu_tag'].append('985')
        total_data['score'] += info.score_map()['985']
    elif np.intersect1d(basic_data['college'], info.college211()).size > 0:
        total_data['tag']['edu_tag'].append('211')
        total_data['score'] += info.score_map()['211']

    # 给籍贯加tag
    if len(basic_data['loc']) > 0:
        loc_pattern = '|'.join(info.province())
        for loc in basic_data['loc']:
            matches = re.findall(loc_pattern, loc)
            if matches:
                total_data['tag']['loc_tag'] = matches[0]
                break

    # 最高学历加tag
    if len(basic_data['edu']) > 0:
        total_data['tag']['edu_tag'].append(basic_data['edu'])
        total_data['score'] += info.score_map()[basic_data['edu']]

    # 删除空字段
    key_to_del = []
    for key, value in basic_data.items():
        if value == '' or value == [] or value == 0:
            key_to_del.append(key)
    for key in key_to_del:
        del basic_data[key]