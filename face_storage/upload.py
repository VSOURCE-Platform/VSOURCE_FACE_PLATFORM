# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : upload.py
# @Function : TODO

from werkzeug.utils import secure_filename
from flask import Blueprint
from app import app

import traceback
import flask
import time
import os

upload_api = Blueprint('upload', __name__)


@upload_api.route('/face_upload', methods=['POST'])
def face_upload():
    def allowed_file(filename):
        # 获取文件扩展名，以'.'为右分割然后取第二个值
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ['jpg', 'png']

    if 'file' not in flask.request.files:
        return flask.jsonify({'status': 500, 'err_msg': '[Face_Storage] No file in files'})
    file = flask.request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploader_folder = app.config['UPLOAD_FOLDER']
        save_dir = os.path.join(uploader_folder, 'face_recognition')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '-' + str(time.time() - int(time.time()))[2:5]
        filepath = os.path.join(timestamp, filename)
        if not os.path.exists(os.path.join(save_dir, timestamp)):
            os.makedirs(os.path.join(save_dir, timestamp))
        file.save(os.path.join(save_dir, filepath))
        return flask.jsonify({'status': 200, 'return_path': filepath,
                              'timestamp': timestamp, 'filename': filename})
    return flask.jsonify({'status': 500})

@upload_api.route('/get_image_file/<timestamp>/<filename>')
def face_file(timestamp, filename):
    try:
        uploader_folder = app.config['UPLOAD_FOLDER']
        save_dir = os.path.join(uploader_folder, 'face_recognition')
        file_path = os.path.join(save_dir, timestamp, filename)
        return flask.send_file(file_path) # flask.Response
    except Exception as e:
        traceback.print_exc()
        return flask.jsonify({'status': 500, 'err_msg': str(e)})

@upload_api.route('/speaker_upload', methods=['POST'])
def speaker_upload():
    def allowed_file(filename):
        # 获取文件扩展名，以'.'为右分割然后取第二个值
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ['wav', 'mp3']

    if 'file' not in flask.request.files:
        return flask.jsonify({'status': 500, 'err_msg': '[Face_Storage] No file in files'})

    file = flask.request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploader_folder = app.config['UPLOAD_FOLDER']
        save_dir = os.path.join(uploader_folder, 'speaker_recognition')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '-' + str(time.time() - int(time.time()))[2:5]
        filepath = os.path.join(timestamp, filename)
        if not os.path.exists(os.path.join(save_dir, timestamp)):
            os.makedirs(os.path.join(save_dir, timestamp))
        file.save(os.path.join(save_dir, filepath))
        return flask.jsonify({'status': 200, 'return_path': filepath,
                              'timestamp': timestamp, 'filename': filename})
    return flask.jsonify({'status': 500})

@upload_api.route('/get_speaker_file/<timestamp>/<filename>')
def speaker_file(timestamp, filename):
    try:
        uploader_folder = app.config['UPLOAD_FOLDER']
        save_dir = os.path.join(uploader_folder, 'speaker_recognition')
        file_path = os.path.join(save_dir, timestamp, filename)
        return flask.send_file(file_path) # flask.Response
    except Exception as e:
        traceback.print_exc()
        return flask.jsonify({'status': 500, 'err_msg': str(e)})
