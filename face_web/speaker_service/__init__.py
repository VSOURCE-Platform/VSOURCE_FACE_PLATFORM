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

speaker_service_print = flask.Blueprint('speaker_service_print', __name__)

@speaker_service_print.route('/speaker_submit', methods=['POST'])
@upper_visitor
def speaker_submit():
    ans = {'status': 200, 'err_msg': ''}
    try:
        speaker_name1 = flask.request.form.get('speaker_name1')
        speaker_name2 = flask.request.form.get('speaker_name2')
        print(speaker_name1, speaker_name2)
        info = {
            'id': str(uuid.uuid1()),
            'speaker_name1': speaker_name1,
            'speaker_name2': speaker_name2,
            'status': 'unfinished',
            'owner': flask_login.current_user.id,
            'create_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        info_str = json.dumps(info)
        producer = kafka.KafkaProducer(bootstrap_servers=[configs.app_kafka_host])
        future = producer.send(configs.app_kafka_speaker_topic, key=bytes(configs.app_kafka_speaker_key, encoding='utf-8'), value=bytes(info_str, encoding='utf-8'))
        producer.close()
        try:
            future.get(timeout=5)  # 监控是否发送成功
        except Exception as e:  # 发送失败抛出kafka_errors
            traceback.print_exc()
        ans['id'] = info['id']
        ans['speaker_name1'] = info['speaker_name1']
        ans['speaker_name2'] = info['speaker_name2']
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
    return ans

@speaker_service_print.route('/speaker_upload', methods=['POST'])
@upper_visitor
def speaker_upload():
    if 'file' not in flask.request.files:
        return flask.jsonify({'status': 500, 'err_msg': '[Face_Web] No file in files'})

    print(flask.request.files['file'])
    file = flask.request.files['file']
    files = {
        'file': (file.filename, file.read(), file.content_type)
    }
    upload_url = configs.app_storage_host + configs.app_speaker_storage_interface
    response = requests.post(upload_url, files=files)
    print(response.text)
    return response.text

@speaker_service_print.route('/get_speaker_file/<timestamp>/<filename>')
def speaker_file(timestamp, filename):
    try:
        get_file_url = configs.app_storage_host + configs.app_speaker_storage_getfile_interface + '/' + timestamp + '/' + filename
        result = requests.get(get_file_url)
        response = make_response(result.content)
        response.headers = dict(result.headers)
        return response
    except Exception as e:
        traceback.print_exc()
        return flask.jsonify({'status': 500, 'err_msg': str(e)})

@speaker_service_print.route('/web/speaker_data')
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