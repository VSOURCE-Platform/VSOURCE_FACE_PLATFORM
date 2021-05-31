# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : service.py
# @Function : TODO

import copy
import flask_login

from app import app, db
import configs

def get_data_from_page_limit(page, limit):
    results = db[configs.app_face_detection_table_name].find()
    ans_data = []
    for each_result in results:
        _message = {}
        _id = each_result['id']
        _message['id'] = each_result['id']
        _message['status'] = each_result['status']
        _message['createDate'] = each_result['create_date']
        _message['face_name1'] = each_result['face_name1']
        _message['face_name1'] = '<img width=\"50px\" height=\"50px\" src=\"/get_face_detection_file/{}\">'.format( each_result['face_name1'])
        _message['face_name2'] = each_result['face_name2']
        _message['face_name2'] = '<img width=\"50px\" height=\"50px\" src=\"/get_face_detection_file/{}\">'.format(each_result['face_name2'])
        if 'owner' not in dict(each_result).keys():
            _message['owner'] = 'debug'
        else:
            _message['owner'] = each_result['owner']
        ans_data.append(_message)

    final_data = []
    start_ind = (page - 1) * limit
    end_ind = page * limit
    if start_ind >= len(ans_data):
        final_data = []
    else:
        sorted_data = sorted(ans_data, key=lambda x: x['createDate'], reverse=True)
        final_data = sorted_data[start_ind: end_ind]
    return final_data, len(ans_data)