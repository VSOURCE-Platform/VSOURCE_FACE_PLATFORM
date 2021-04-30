# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : configs.py
# @Function : TODO

app_redis_hostname = 'localhost'
app_redis_port     = 6379

app_info_key = 'INFO_KEY'
app_response_key = 'RESPONSE_KEY'

app_database_host = 'my_mongo' # if don't use docker, so this is 'localhost'
app_database_name = 'face_recognition'
app_database_user = 'xcy'
app_database_pwd  = 'xcy123456'
app_database_port = 27017

app_database_table_name = 'face_list'

app_mongo_uri  = "mongodb://{}:{}@{}:{}".format(
    app_database_user,
    app_database_pwd,
    app_database_host,
    app_database_port
)

call_interval = 0.1