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

from speaker_recognition_native_api.speaker_api import get_vs_object, voice_recognition


class Service:
    def __init__(self):
        self.redis_host = configs.app_redis_hostname
        self.redis_port = configs.app_redis_port
        self.INFO_KEY = configs.app_info_key
        self.RESPONSE_KEY = configs.app_response_key
        self.SPEAKER_ERROR_KEY = configs.app_speaker_error_key
        self.group_id = configs.app_group_id

    def start(self):
        print('[Calculator Init] Speaker Recognition Service Starting...')
        print('[Calculator Init] GET VS OBJECT...')
        vs = get_vs_object()
        r = redis.Redis(host=self.redis_host, port=self.redis_port)
        print('[Calculator Init] GET VS OBJECT OK!')
        time.sleep(configs.sleep_interval)
        print('[Calculator Init] Init Successfully!')
        while True:
            try:
                consumer = kafka.KafkaConsumer(configs.app_kafka_topic,
                                               group_id=self.group_id
                                               ,bootstrap_servers=[configs.app_kafka_host])
                for msg in consumer:
                    try:
                        info_str = msg.value
                        if not info_str or info_str is None:
                            time.sleep(configs.call_interval)
                            continue

                        info_str = str(info_str, encoding = "utf-8")
                        print(info_str)
                        info = json.loads(info_str)
                        speech1 = info['speaker_name1']
                        speech2 = info['speaker_name2']
                        speech_file_inerface = configs.app_web_host + configs.app_file_interface + '/'
                        speech_url1 = speech_file_inerface + speech1
                        speech_url2 = speech_file_inerface + speech2
                        score = voice_recognition(vs, speech_url1, speech_url2)

                        ans = copy.deepcopy(info)
                        ans['status'] = 'finished'
                        ans['score'] = str(round(score, 3))
                        ans_str = json.dumps(ans)
                        assert r.rpush(self.RESPONSE_KEY, ans_str)
                    except Exception as e:
                        traceback.print_exc()
                        assert r.rpush(self.SPEAKER_ERROR_KEY, ans_str)
                        continue
            except Exception as e:
                traceback.print_exc()
                time.sleep(configs.call_interval)
                continue


if __name__ == '__main__':
    service = Service()
    service.start()

    # vs = get_vs_object()
    # speech1 = '/Users/ecohnoch/Desktop/face_service/speaker_calculator/face_recognition_native_api/tmp/0.wav'
    # speech2 = '/Users/ecohnoch/Desktop/face_service/speaker_calculator/face_recognition_native_api/tmp/1.wav'
    # score = voice_recognition(vs, speech1, speech2)
    # print(score)