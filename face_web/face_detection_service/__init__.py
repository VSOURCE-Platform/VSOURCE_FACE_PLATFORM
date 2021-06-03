# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : __init__.py
# @Function : TODO

from flask import request, make_response
from app import app, db

import uuid
import json
import time
import flask
import redis
import requests
import traceback

import configs

import flask_login
import face_detection_service.service as service
from flask_cors import cross_origin
from login import upper_visitor

face_detection_service_print = flask.Blueprint('face_detection_service_print', __name__)


@face_detection_service_print.route('/face_detection_submit', methods=['POST'])
@upper_visitor
def face_detection_submit():
    ans = {'status': 200, 'err_msg': ''}
    info = {
        'id': str(uuid.uuid1()),
        'status': 'unfinished',
        'owner': flask_login.current_user.id,
        'create_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    try:
        face_name = flask.request.form.get('face_name')
        info['face_name1'] = face_name
        face_detection_url = configs.face_detection_url
        response = requests.get(face_detection_url, params={'image_path': face_name})
        response_dict = json.loads(response.content)
        info['face_name2'] = response_dict['return_path']
        info['status'] = 'finished'
        db[configs.app_face_detection_table_name].insert_one(info)
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
        info['status'] = 'error'
        info['err_msg'] = str(e)
        db[configs.app_face_detection_table_name].insert_one(info)
    return ans


@face_detection_service_print.route('/face_detection/get_result', methods=['GET'])
@upper_visitor
def get_face_detection_result():
    ans = {'status': 200, 'err_msg': ''}
    info = {
        'id': str(uuid.uuid1()),
        'status': 'unfinished',
        'owner': flask_login.current_user.id,
        'create_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    try:
        image_path = request.args.get('image_path')
        info['face_name1'] = image_path
        face_detection_url = configs.face_detection_url
        response = requests.get(face_detection_url, params={'image_path': image_path})
        response_dict = json.loads(response.content)
        info['face_name2'] = response_dict['return_path']
        info['status'] = 'finished'
        info['result'] = response_dict['result']
        ans['result'] = info
        db[configs.app_face_detection_table_name].insert_one(info)
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
        info['status'] = 'error'
        info['err_msg'] = str(e)
        db[configs.app_face_detection_table_name].insert_one(info)
    return ans


@face_detection_service_print.route('/face_detection_upload', methods=['POST'])
@upper_visitor
def face_detection_upload():
    if 'file' not in flask.request.files:
        return flask.jsonify({'status': 500, 'err_msg': '[Face_Web] No file in files'})

    file = flask.request.files['file']
    files = {
        'file': (file.filename, file.read(), file.content_type)
    }
    response = requests.post(configs.face_detection_upload_url, files=files)
    print(response.text)
    return response.text


@face_detection_service_print.route('/get_face_detection_file/<timestamp>/<filename>')
def face_detection_file(timestamp, filename):
    try:
        face_get_file_url = configs.face_detection_get_url + '/' + timestamp + '/' + filename
        result = requests.get(face_get_file_url)
        response = make_response(result.content)
        response.headers = dict(result.headers)
        return response
    except Exception as e:
        traceback.print_exc()
        return flask.jsonify({'status': 500, 'err_msg': str(e)})


@face_detection_service_print.route('/web/face_detection_data')
@cross_origin()
# @upper_visitor
@flask_login.login_required
def get_face_detection_data_interface():
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