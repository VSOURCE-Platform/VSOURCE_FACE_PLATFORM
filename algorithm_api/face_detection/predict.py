#----------------------------------------------------#
#   对视频中的predict.py进行了修改，
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
import os
import cv2
import time
import json
import flask
import requests
import traceback
import numpy as np
import tensorflow as tf
import keras

from urllib import request

import configs
from retinaface import Retinaface

app = flask.Flask(__name__)

global graph, sess
graph = tf.get_default_graph()
sess = keras.backend.get_session()
with sess.as_default():
    with graph.as_default():
        retinaface = Retinaface()

@app.route('/face_detection')
def face_detection():
    ans = {'status': 200, 'err_msg': ''}
    try:
        image_path = flask.request.args.get('image_path')
        face_image = configs.get_url + '/' + image_path
        face_image = request.urlopen(face_image)
        face_image = cv2.imdecode(np.asarray(bytearray(face_image.read()), dtype="uint8"), cv2.IMREAD_COLOR)
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        print(face_image.shape)
        with graph.as_default():
            r_image = retinaface.detect_image(face_image)
        r_image = cv2.cvtColor(r_image, cv2.COLOR_RGB2BGR)
        filename = os.path.split(image_path)[-1]
        response = requests.post(configs.upload_url, files={
            'file': (filename + '.jpg', cv2.imencode(".jpg", r_image)[1].tobytes(), 'image/jpg')
        })
        response_dict = json.loads(response.content)
        print(response_dict['return_path'])
        ans['return_path'] = response_dict['return_path']
        return flask.jsonify(ans)
    except Exception as e:
        traceback.print_exc()
        ans['status'] = 400
        ans['err_msg'] = str(e)
        return ans


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configs.port, debug=True)