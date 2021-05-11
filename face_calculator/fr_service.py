import os
import copy
import time
import json
import redis
import kafka
import requests
import traceback
from urllib import request


import configs

from face_recognition_native_api.face_api import get_fs_object, face_recognition, face_recognition_with_image

class Service:
    def __init__(self):
        self.redis_host = configs.app_redis_hostname
        self.redis_port = configs.app_redis_port
        self.INFO_KEY = configs.app_info_key
        self.RESPONSE_KEY = configs.app_response_key
        self.group_id = configs.app_group_id

    def start(self):
        print('[Calculator Init] FR SERVICE RUNNING...')
        print('[Calculator Init] GET FS OBJECT...')
        fs = get_fs_object()
        r = redis.Redis(host=self.redis_host, port=self.redis_port)
        print('[Calculator Init] GET FS OBJECT OK!')
        while True:
            try:
                consumer = kafka.KafkaConsumer(configs.app_kafka_topic,
                                               group_id=self.group_id
                                               ,bootstrap_servers=[configs.app_kafka_host])
                for msg in consumer:
                    info_str = msg.value
                    if not info_str or info_str is None:
                        time.sleep(configs.call_interval)
                        continue

                    info_str = str(info_str, encoding = "utf-8")
                    print(info_str)
                    info = json.loads(info_str)
                    face1 = info['face_name1']
                    face2 = info['face_name2']
                    face_file_inerface = configs.app_web_host + configs.app_file_interface + '/'
                    real_face1 = request.urlopen(face_file_inerface + face1)
                    real_face2 = request.urlopen(face_file_inerface + face2)
                    score = face_recognition_with_image(fs, real_face1, real_face2)

                    ans = copy.deepcopy(info)
                    ans['status'] = 'finished'
                    ans['score'] = str(round(score, 3))
                    # ans = {'id': info['id'], 'score': str(score)}
                    ans_str = json.dumps(ans)
                    assert r.rpush(self.RESPONSE_KEY, ans_str)
            except Exception as e:
                traceback.print_exc()
                time.sleep(configs.call_interval)
                continue


if __name__ == '__main__':
    service = Service()
    service.start()

    # face1 = './work/face_recognition_native_api/tmp/0006_01.jpg'
    # face2 = './work/face_recognition_native_api/tmp/0007_01.jpg'
    # score = face_recognition(face1, face2)
    # print(score)