# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : configs.py
# @Function : TODO


app_port = 12349
app_secret_key = 'fr_service'

app_redis_hostname = 'my_redis'
app_redis_port     = 6379

app_info_key = 'INFO_KEY'
app_response_key = 'RESPONSE_KEY'
app_result_key = 'RESULT_KEY'

app_kafka_host = 'my_kafka:9092'
app_kafka_topic = 'user_queue'
app_kafka_key = 'user_requests'


app_database_host = 'my_mongo' # if don't use docker, so this is 'localhost'
app_database_name = 'face_recognition'
app_database_table = 'face_list'
app_database_user = 'xcy'
app_database_pwd  = 'xcy123456'
app_database_port = 27017

app_database_table_name = 'face_list'
app_database_request_table = 'face_requests'

app_mongo_uri  = "mongodb://{}:{}@{}:{}/{}".format(
    app_database_user,
    app_database_pwd,
    app_database_host,
    app_database_port,
    app_database_name
)

app_storage_host = 'http://face_storage:12350'
app_storage_interface = '/face_upload'
app_storage_getfile_interface = '/get_image_file'