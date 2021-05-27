# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : configs.py
# @Function : TODO

app_kafka_host = 'my_kafka:9092'
app_kafka_topic = 'user_queue'
app_kafka_key = 'user_requests'
app_group_id  = 'request_db'
app_kafka_speaker_topic = 'speaker_queue'
app_kafka_speaker_key = 'speaker_requests'

app_database_host = 'my_mongo' # if don't use docker, so this is 'localhost'
app_database_name = 'face_recognition'
app_database_user = 'xcy'
app_database_pwd  = 'xcy123456'
app_database_port = 27017

app_database_request_table = 'face_requests'
app_speaker_request_table = 'speaker_requests'

call_interval = 0.1
sleep_interval = 15