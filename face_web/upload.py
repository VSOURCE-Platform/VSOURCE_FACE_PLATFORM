# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : upload.py
# @Function : TODO

from flask import request, render_template
from werkzeug.utils import secure_filename
from flask import Blueprint
from app import app, db

import configs

import traceback
import flask
import kafka
import copy
import json
import time
import uuid
import os

upload_api = Blueprint('upload', __name__, template_folder='./templates', static_folder='./static')

@upload_api.route('/submit_page')
def submit_page():
    return render_template('submit_page.html')

@upload_api.route('/face_upload', methods=['POST'])
def face_upload():
    def allowed_file(filename):
        # 获取文件扩展名，以'.'为右分割然后取第二个值
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ['jpg', 'png']

    if 'file' not in flask.request.files:
        return flask.jsonify({'code': 1})
    file = flask.request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploader_folder = app.config['UPLOAD_FOLDER']
        save_dir = os.path.join(uploader_folder, 'face_recognition')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '-' + str(time.time() - int(time.time()))[2:5]
        filename = os.path.join(timestamp, filename)
        if not os.path.exists(os.path.join(save_dir, timestamp)):
            os.makedirs(os.path.join(save_dir, timestamp))
        file.save(os.path.join(save_dir, filename))
        return flask.jsonify({'code': -1, 'return_path': filename})
    return flask.jsonify({'code': 1})

@upload_api.route('/get_image_file/<timestamp>/<filename>')
def face_file(timestamp, filename):
    try:
        uploader_folder = app.config['UPLOAD_FOLDER']
        save_dir = os.path.join(uploader_folder, 'face_recognition')
        file_path = os.path.join(save_dir, timestamp, filename)
        return flask.send_file(file_path)
    except Exception as e:
        traceback.print_exc()
        return flask.jsonify({'error': 1, 'err_msg': str(e)})

@upload_api.route('/face_submit', methods=['GET', 'POST'])
def face_submit():
    if flask.request.method == 'GET':
        return render_template('main.html')
    ans = {'status': 200, 'err_msg': ''}
    try:
        face_name1 = flask.request.form.get('face_name1')
        face_name2 = flask.request.form.get('face_name2')
        print(face_name1, face_name2)
        uploader_folder = app.config['UPLOAD_FOLDER']
        save_dir = os.path.join(uploader_folder, 'face_recognition')
        face_path1 = os.path.join(save_dir, face_name1)
        face_path2 = os.path.join(save_dir, face_name2)
        info = {
            'id': str(uuid.uuid1()),
            'face_name1': face_name1,
            'face_name2': face_name2,
            'face1': face_path1,
            'face2': face_path2,
            'create_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        # 写入数据库
        auth_ans = db.authenticate(name=configs.app_database_user, password=configs.app_database_pwd)
        request_record = copy.deepcopy(info)
        request_record['status'] = 'unfinished'
        insert_result = db[configs.app_database_request_table].insert_one(request_record)

        info_str = json.dumps(info)
        producer = kafka.KafkaProducer(bootstrap_servers=[configs.app_kafka_host])
        future = producer.send(configs.app_kafka_topic, key=bytes(configs.app_kafka_key, encoding='utf-8'),
                               value=bytes(info_str, encoding='utf-8'))
        producer.close()
        try:
            future.get(timeout=5)  # 监控是否发送成功
        except Exception as e:  # 发送失败抛出kafka_errors
            traceback.format_exc()
        ans['id'] = info['id']
        ans['face_name1'] = info['face_name1']
        ans['face_name2'] = info['face_name2']
    except Exception as e:
        ans['status'] = 500
        ans['err_msg'] = str(e)
    return ans
