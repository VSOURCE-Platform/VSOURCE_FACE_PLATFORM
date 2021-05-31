# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : service.py
# @Function : TODO

import copy
import flask_login

from app import app, db
import configs

def get_data_from_page_limit(page, limit):
    all_requests = db[configs.app_database_request_table].find()
    results = db[configs.app_database_table].find()
    ans_data = []
    for each_request in all_requests:
        _message = {}
        _id = each_request['id']
        this_result = db[configs.app_database_table].find_one({'id': str(_id)})
        if this_result:
            # 任务已经结束，拿到任务的所有信息
            each_result = copy.deepcopy(this_result)
            _message['id'] = each_result['id']
            _message['status'] = each_result['status']
            _message['createDate'] = each_result['create_date']
            _message['collectedDate'] = each_result['collected_date']
            _message['face_name1'] = "/get_image_file/" + each_result['face_name1']
            # _message['face_name1'] = '<img width=\"50px\" height=\"50px\" src=\"/get_image_file/{}\">'.format(
                # each_result['face_name1'])
            _message['face_name2'] = "/get_image_file/" +  each_result['face_name2']
            # _message['face_name2'] = '<img width=\"50px\" height=\"50px\" src=\"/get_image_file/{}\">'.format(
            #     each_result['face_name2'])
            _message['score'] = each_result['score']
            if 'owner' not in dict(each_result).keys():
                _message['owner'] = 'debug'
            else:
                _message['owner'] = each_result['owner']
        else:
            # 任务暂未结束，拿到用户信息和状态
            _message['id'] = each_request['id']
            _message['status'] = each_request['status']
            _message['createDate'] = each_request['create_date']
            if 'owner' not in dict(each_request).keys():
                _message['owner'] = 'debug'
            else:
                _message['owner'] = each_request['owner']

        if _message['owner'] == flask_login.current_user.id:
            # TODO 如果是正常的用户，只加入该用户的数据，这里应该在db层解决，待优化
            ans_data.append(_message)
            continue
        if _message['owner'] == 'debug' and flask_login.current_user.is_visitor():
            # 如果是游客，加入debug用户的数据
            ans_data.append(_message)
            continue

    final_data = []
    start_ind = (page - 1) * limit
    end_ind = page * limit
    if start_ind >= len(ans_data):
        final_data = []
    else:
        sorted_data = sorted(ans_data, key=lambda x: x['createDate'], reverse=True)
        final_data = sorted_data[start_ind: end_ind]
    return final_data, len(ans_data)