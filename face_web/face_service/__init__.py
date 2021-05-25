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

import flask_login
import face_service.service as service
from flask_cors import cross_origin
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

    final_data, cnt = service.get_data_from_page_limit(page, limit)

    head["data"] = final_data
    head["count"] = cnt
    return flask.jsonify(head)