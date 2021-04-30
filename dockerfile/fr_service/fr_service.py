import time
import json
import redis
import traceback


import numpy as np
from dockerfile.my_web import configs


def face_recognition(face_image1, face_image2):
    time.sleep(5)
    return np.random.randint(0, 100) / 100

class Service:
    def __init__(self):
        self.redis_host = configs.app_redis_hostname
        self.redis_port = configs.app_redis_port
        self.INFO_KEY = configs.app_info_key
        self.RESPONSE_KEY = configs.app_response_key

    def start(self):
        while True:
            try:
                r = redis.Redis(host=self.redis_host, port=self.redis_port)
                info_str = r.lpop(self.INFO_KEY)
                if not info_str or info_str is None:
                    time.sleep(configs.call_interval)
                    continue

                info_str = str(info_str, encoding = "utf-8")
                print(info_str)
                info = json.loads(info_str)
                score = face_recognition(info['face1'], info['face2'])
                ans = {'id': info['id'], 'score': str(score)}
                ans_str = json.dumps(ans)
                assert r.rpush(self.RESPONSE_KEY, ans_str)
            except Exception as e:
                traceback.print_exc()
                time.sleep(configs.call_interval)
                continue


if __name__ == '__main__':
    service = Service()
    service.start()