# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : configs.py
# @Function : TODO

app_redis_hostname = 'my_redis'
app_redis_port     = 6379

app_info_key = 'INFO_KEY'
app_response_key = 'RESPONSE_KEY'
app_error_key = 'ERROR_KEY'
app_speaker_info_key = 'SPEAKER_INFO_KEY'
app_speaker_response_key = 'SPEAKER_RESPONSE_KEY'
app_speaker_error_key = 'SPEAKER_ERROR_KEY'

app_database_host = 'my_mongo' # if don't use docker, so this is 'localhost'
app_database_name = 'face_recognition'
app_database_user = 'xcy'
app_database_pwd  = 'xcy123456'
app_database_port = 27017

app_face_table_name = 'face_list'
app_face_request_table = 'face_requests'
app_speaker_table_name = 'speaker_list'
app_speaker_request_table = 'speaker_requests'

call_interval = 0.1
max_interval = 3
sleep_interval = 10