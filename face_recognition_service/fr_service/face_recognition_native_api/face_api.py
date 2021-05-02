# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : face_api.py
# @Function : TODO

from .face_score import FaceScore
from . import configs as configs

def face_recognition(face_path1, face_path2):
    fs = FaceScore(params=configs.face_recognition_params)
    return fs.cal_score(face_path1, face_path2)

if __name__ == '__main__':
    face1 = '/Users/ecohnoch/Desktop/face_service/face_score/tmp/0006_01.jpg'
    face2 = '/Users/ecohnoch/Desktop/face_service/face_score/tmp/0007_01.jpg'
    score = face_recognition(face1, face2)
    print(score)