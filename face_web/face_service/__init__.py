# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : __init__.py
# @Function : TODO

from flask import request, make_response
from app import app, db

import uuid
import copy
import json
import time
import kafka
import flask
import redis
import requests
import traceback

import configs

from flask_cors import cross_origin
import flask_login
from login import upper_visitor

face_service_print = flask.Blueprint('face_service_print', __name__)

@face_service_print.route('/face_submit', methods=['POST'])
@upper_visitor
def face_submit():
    ans = {'status': 200, 'err_msg': ''}
    try:
        face_name1 = flask.request.form.get('face_name1')
        face_name2 = flask.request.form.get('face_name2')
        print(face_name1, face_name2)
        info = {
            'id': str(uuid.uuid1()),
            'face_name1': face_name1,
            'face_name2': face_name2,
            'status': 'unfinished',
            'owner': flask_login.current_user.id,
            'create_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        info_str = json.dumps(info)
        producer = kafka.KafkaProducer(bootstrap_servers=[configs.app_kafka_host])
        future = producer.send(configs.app_kafka_topic, key=bytes(configs.app_kafka_key, encoding='utf-8'),
                               value=bytes(info_str, encoding='utf-8'))
        producer.close()
        try:
            future.get(timeout=5)  # 监控是否发送成功
        except Exception as e:  # 发送失败抛出kafka_errors
            traceback.print_exc()
        ans['id'] = info['id']
        ans['face_name1'] = info['face_name1']
        ans['face_name2'] = info['face_name2']
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
    return ans


@face_service_print.route('/get_result', methods=['GET'])
@upper_visitor
def get_result():
    ans = {'status': 200, 'err_msg': ''}
    try:
        uu_id = request.args.get('id')
        uu_id = str(uu_id)

        r = redis.Redis(host=configs.app_redis_hostname, port=configs.app_redis_port)
        if r.get(uu_id):
            print('From redis get this result.')
            return r.get(uu_id)
        else:
            auth_ans = db.authenticate(name=configs.app_database_user, password=configs.app_database_pwd)
            result = db[configs.app_database_table].find_one({'id': uu_id})
            result.pop('_id')
            ans['result'] = result
            r.set(uu_id, ans)
            r.expire(uu_id, configs.app_redis_expire_time)
            print('Write into redis')
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
    return ans



@face_service_print.route('/face_upload', methods=['POST'])
@upper_visitor
def face_upload():
    if 'file' not in flask.request.files:
        return flask.jsonify({'status': 500, 'err_msg': '[Face_Web] No file in files'})

    print(flask.request.files['file'])
    file = flask.request.files['file']
    files = {
        'file': (file.filename, file.read(), file.content_type)
    }
    face_upload_url = configs.app_storage_host + configs.app_storage_interface
    response = requests.post(face_upload_url, files=files)
    print(response.text)
    return response.text

@face_service_print.route('/get_image_file/<timestamp>/<filename>')
def face_file(timestamp, filename):
    try:
        face_get_file_url = configs.app_storage_host + configs.app_storage_getfile_interface + '/' + timestamp + '/' + filename
        result = requests.get(face_get_file_url)
        response = make_response(result.content)
        response.headers = dict(result.headers)
        return response
    except Exception as e:
        traceback.print_exc()
        return flask.jsonify({'status': 500, 'err_msg': str(e)})

@face_service_print.route('/get_scaled_image_file/<timestamp>/<filename>')
def get_scaled_face_file(timestamp, filename):
    try:
        face_get_file_url = configs.app_storage_host + configs.app_storage_getfile_interface + '/' + timestamp + '/' + filename
        result = requests.get(face_get_file_url)
        response = make_response(result.content)
        response.headers = dict(result.headers)
        return response
    except Exception as e:
        traceback.print_exc()
        return flask.jsonify({'status': 500, 'err_msg': str(e)})

@face_service_print.route('/web/face_data')
@cross_origin()
# @upper_visitor
@flask_login.login_required
def get_face_data_interface():
    head = {"code": 0, "msg": "", "count": 10000, "data": []}
    limit = int(request.values.get('limit'))
    page = int(request.values.get('page'))
    if not limit:
        limit = 10
    if not page:
        page = 1

    all_requests = db[configs.app_database_request_table].find()
    results = db[configs.app_database_table].find()
    ans_data = []
    for each_request in all_requests:
        _message = {}
        _id = each_request['id']
        task_finished = -1
        for idx, each_result in enumerate(results):
            if _id == each_result['id']:
                task_finished = idx
                break
        if task_finished != -1:
            # 任务已经结束，拿到任务的所有信息
            each_result = list(results)[task_finished]
            _message['id'] = each_result['id']
            _message['status'] = each_result['status']
            _message['createDate'] = each_result['create_date']
            _message['collectedDate'] = each_result['collected_date']
            _message['face_name1'] = each_result['face_name1']
            _message['face_name1'] = '<img width=\"50px\" height=\"50px\" src=\"/get_image_file/{}\">'.format(
                each_result['face_name1'])
            _message['face_name2'] = each_result['face_name2']
            _message['face_name2'] = '<img width=\"50px\" height=\"50px\" src=\"/get_image_file/{}\">'.format(
                each_result['face_name2'])
            _message['score'] = each_result['score']
            if 'owner' not in dict(each_result).keys():
                _message['owner'] = each_result['owner']
            else:
                _message['owner'] = 'debug'
        else:
            # 任务暂未结束，拿到用户信息和状态
            _message['id'] = each_request['id']
            _message['status'] = each_request['status']
            _message['createDate'] = each_request['create_date']
            if 'owner' not in dict(each_request).keys():
                _message['owner'] = each_request['owner']
            else:
                _message['owner'] = 'debug'

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
        final_data = sorted_data[start_ind : end_ind]

    head["data"] = final_data
    head["count"] = len(ans_data)
    return flask.jsonify(head)