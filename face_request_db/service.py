import time
import json
import copy
import kafka
import pymongo
import traceback

import configs

class Service:
    def __init__(self):
        self.kafka_topic = configs.app_kafka_topic
        self.kafka_host = configs.app_kafka_host
        self.group_id    = configs.app_group_id
        self.mongo_host  = configs.app_database_host
        self.mongo_port  = configs.app_database_port
        self.mongo_db   = configs.app_database_name
        self.mongo_user  = configs.app_database_user
        self.mongo_pwd   = configs.app_database_pwd
        self.request_table = configs.app_database_request_table

    def start(self):
        print('Running...')
        while True:
            try:
                consumer = kafka.KafkaConsumer(self.kafka_topic,
                                               group_id=self.group_id
                                               ,bootstrap_servers=[self.kafka_host])
                for msg in consumer:
                    info_str = msg.value
                    if not info_str or info_str is None:
                        time.sleep(configs.call_interval)
                        continue

                    info_str = str(info_str, encoding = "utf-8")
                    info = json.loads(info_str)
                    client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port)
                    db = client[self.mongo_db]
                    auth_ans = db.authenticate(name=self.mongo_user, password=self.mongo_pwd)
                    request_record = copy.deepcopy(info)
                    request_record['status'] = 'unfinished'
                    if db[configs.app_database_request_table].find_one({'id':request_record['id']}):
                        request_record['status'] = 'recovered'
                        db[configs.app_database_request_table].save(request_record)
                    else:
                        insert_result = db[configs.app_database_request_table].insert_one(request_record)
                        print('request has been written in db. info: ', info_str)
            except Exception as e:
                traceback.print_exc()
                time.sleep(configs.call_interval)
                continue


if __name__ == '__main__':
    service = Service()
    service.start()