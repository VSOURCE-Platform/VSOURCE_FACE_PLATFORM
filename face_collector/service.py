import time
import json
import redis
import traceback
import pymongo

import configs


class Service:
    def __init__(self):
        self.redis_host = configs.app_redis_hostname
        self.redis_port = configs.app_redis_port
        self.RESPONSE_KEY = configs.app_response_key
        self.SPEAKER_RESPONSE_KEY = configs.app_speaker_response_key

        self.mongo_host  = configs.app_database_host
        self.mongo_port  = configs.app_database_port
        self.mongo_db   = configs.app_database_name
        self.mongo_user  = configs.app_database_user
        self.mongo_pwd   = configs.app_database_pwd

        self.face_table_name = configs.app_face_table_name
        self.face_request_table_name = configs.app_face_request_table

        self.speaker_table_name = configs.app_speaker_table_name
        self.speaker_request_table_name = configs.app_speaker_request_table

    def start(self):
        print('[Collector Init] Sleeping...')
        time.sleep(configs.sleep_interval)
        print('[Collector Init] Init Successfully!')
        while True:
            try:
                r = redis.Redis(host=self.redis_host, port=self.redis_port)
                # 先拉人脸的结果
                mode = 'face_recognition'
                response_str = r.lpop(self.RESPONSE_KEY)

                if not response_str or response_str is None:
                    # 再拉说话人的结果
                    mode = 'speaker_recognition'
                    response_str = r.lpop(self.SPEAKER_RESPONSE_KEY)

                if not response_str or response_str is None:
                    mode = ''
                    time.sleep(configs.call_interval)
                    continue

                if mode == 'face_recognition':
                    table_name = self.face_table_name
                    request_table_name = self.face_request_table_name
                elif mode == 'speaker_recognition':
                    table_name = self.speaker_table_name
                    request_table_name = self.speaker_request_table_name
                else:
                    raise Exception('Error when collecting results, invaild mode: ', mode)

                response_str = str(response_str, encoding = "utf-8")
                print(response_str)
                response = json.loads(response_str)
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                response['collected_date'] = now_time

                client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port)
                db = client[self.mongo_db]
                db.authenticate(name=self.mongo_user, password=self.mongo_pwd)
                table = db[table_name]
                table.insert_one(response)

                request_table = db[request_table_name]
                request_info = request_table.find_one({'id': response['id']})
                if request_info:
                    request_info['status'] = 'finished'
                    request_table.save(request_info)
                else:
                    time.sleep(configs.max_interval)
                    request_table = db[self.request_table_name]
                    request_info = request_table.find_one({'id': response['id']})
                    if not request_info:
                        request_table.insert({'id': response['id'], 'status': 'lost'})
                    else:
                        request_info['status'] = 'finished'
                        request_table.save(request_info)

            except Exception as e:
                traceback.print_exc()
                time.sleep(configs.call_interval)
                continue


if __name__ == '__main__':
    service = Service()
    service.start()