# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : face_api.py
# @Function : TODO

from .speaker_score import VoiceScore
from . import configs as configs

def get_vs_object():
    return VoiceScore(params=configs.speaker_recognition_params)

def voice_recognition(vs, speech_path1, speech_path2):
    return vs.cal_score_from_http(speech_path1, speech_path2)

if __name__ == '__main__':
    speech1 = '/Users/ecohnoch/Desktop/face_service/speaker_calculator/face_recognition_native_api/tmp/0.wav'
    speech2 = '/Users/ecohnoch/Desktop/face_service/speaker_calculator/face_recognition_native_api/tmp/1.wav'
    score = voice_recognition(speech1, speech2)
    print(score)