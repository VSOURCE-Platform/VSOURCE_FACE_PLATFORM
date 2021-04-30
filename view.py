# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : vie.py
# @Function : TODO

from flask import request
from app import app, mongo

import uuid
import json
import redis
import configs

@app.route('/face_service', methods=['GET'])
def user_call_face_service():
    ans = {'status': 200, 'err_msg': ''}
    try:
        face1 = request.args.get('face1')
        face2 = request.args.get('face2')

        info = {
            'id': str(uuid.uuid1()),
            'face1': face1,
            'face2': face2
        }
        info_str = json.dumps(info)

        r = redis.Redis(host=configs.app_redis_hostname, port=configs.app_redis_port)
        r.rpush(configs.app_info_key, info_str)

        ans['id'] = info['id']
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
    return ans


@app.route('/get_result', methods=['GET'])
def get_result():
    ans = {'status': 200, 'err_msg': ''}
    try:
        uu_id = request.args.get('id')
        uu_id = str(uu_id)

        r = redis.Redis(host=configs.app_redis_hostname, port=configs.app_redis_port)

        result = r.get(uu_id)
        result = str(result, encoding='utf-8')
        ans['result'] = result
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
    return ans


