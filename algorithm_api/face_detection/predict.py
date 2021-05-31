#----------------------------------------------------#
#   对视频中的predict.py进行了修改，
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
import os
import cv2
import time
import json
import numpy as np
from urllib import request
import requests

from retinaface import Retinaface

def detect_face(image_path):
    retinaface = Retinaface()
    get_face_url = 'http://face_storage:12350/get_face_detection_file'
    upload_face_url = 'http://face_storage:12350/face_detection_upload'
    face_image = get_face_url + '/' + image_path
    print(face_image)
    face_image = request.urlopen(face_image)
    face_image = cv2.imdecode(np.asarray(bytearray(face_image.read()), dtype="uint8"), cv2.IMREAD_COLOR)
    print(face_image.shape)
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    r_image = retinaface.detect_image(face_image)
    r_image = cv2.cvtColor(r_image,cv2.COLOR_RGB2BGR)
    filename = os.path.split(image_path)[-1]
    response = requests.post(upload_face_url, files={
        'file': (filename + '.jpg', cv2.imencode(".jpg", r_image)[1].tobytes(), 'image/jpg')
    })
    response_dict = json.loads(response.content)
    print(response_dict['return_path'])
    return response_dict['return_path']

if __name__ == "__main__":
    retinaface = Retinaface()

    '''
    predict.py有几个注意点
    1、无法进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用cv2.imread打开图片文件进行预测。
    2、如果想要保存，利用cv2.imwrite("img.jpg", r_image)即可保存。
    3、如果想要获得框的坐标，可以进入detect_image函数，读取(b[0], b[1]), (b[2], b[3])这四个值。
    4、如果想要截取下目标，可以利用获取到的(b[0], b[1]), (b[2], b[3])这四个值在原图上利用矩阵的方式进行截取。
    5、在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
    '''
    image = './img/29.jpeg'
    image = cv2.imread(image)
    image   = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    r_image = retinaface.detect_image(image)
    r_image = cv2.cvtColor(r_image,cv2.COLOR_RGB2BGR)
    print(r_image.shape)
    cv2.imwrite('./after_detect.jpg', r_image)
