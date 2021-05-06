# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : vie.py
# @Function : TODO

from flask import request
from app import app, db

import uuid
import copy
import json
import time
import kafka
import traceback

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
            'face2': face2,
            'create_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        # 写入数据库
        auth_ans = db.authenticate(name=configs.app_database_user, password=configs.app_database_pwd)
        request_record = copy.deepcopy(info)
        request_record['status'] = 'unfinished'
        insert_result = db[configs.app_database_request_table].insert_one(request_record)

        info_str = json.dumps(info)
        producer = kafka.KafkaProducer(bootstrap_servers=[configs.app_kafka_host])
        future = producer.send(configs.app_kafka_topic, key=bytes(configs.app_kafka_key, encoding='utf-8'), value=bytes(info_str, encoding='utf-8'))
        producer.close()
        try:
            future.get(timeout=5) # 监控是否发送成功
        except Exception as e:  # 发送失败抛出kafka_errors
            traceback.format_exc()

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

        auth_ans = db.authenticate(name=configs.app_database_user, password=configs.app_database_pwd)
        print(auth_ans)
        result = db[configs.app_database_table].find_one({'id': uu_id})
        result.pop('_id')
        ans['result'] = result
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
    return ans


