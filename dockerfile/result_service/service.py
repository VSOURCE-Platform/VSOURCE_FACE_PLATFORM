import time
import json
import redis
import traceback
import pymongo

from dockerfile.my_web import configs


class Service:
    def __init__(self):
        self.redis_host = configs.app_redis_hostname
        self.redis_port = configs.app_redis_port
        self.RESPONSE_KEY = configs.app_response_key
        self.mongo_host  = configs.app_database_host
        self.mongo_port  = configs.app_database_port
        self.mongo_db   = configs.app_database_name
        self.mongo_user  = configs.app_database_user
        self.mongo_pwd   = configs.app_database_pwd
        self.mongo_table = configs.app_database_table_name

    def start(self):
        print('Running...')
        while True:
            try:
                r = redis.Redis(host=self.redis_host, port=self.redis_port)
                response_str = r.lpop(self.RESPONSE_KEY)
                if not response_str or response_str is None:
                    time.sleep(configs.call_interval)
                    continue

                response_str = str(response_str, encoding = "utf-8")
                print(response_str)
                response = json.loads(response_str)
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                response['collected_time'] = now_time

                client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port)
                db = client[self.mongo_db]
                db.authenticate(name=self.mongo_user, password=self.mongo_pwd)
                table = db[self.mongo_table]
                table.insert_one(response)

                # response_str = json.dumps(response)
                # assert r.set(response['id'], response_str)
            except Exception as e:
                traceback.print_exc()
                time.sleep(configs.call_interval)
                continue


if __name__ == '__main__':
    service = Service()
    service.start()