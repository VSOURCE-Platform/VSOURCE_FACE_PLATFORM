# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : configs.py
# @Function : TODO

app_redis_hostname = 'my_redis'
app_redis_port     = 6379
app_info_key = 'SPEAKER_INFO_KEY'
app_response_key = 'SPEAKER_RESPONSE_KEY'
app_speaker_error_key = 'SPEAKER_ERROR_KEY'

app_kafka_host = 'my_kafka:9092'
app_kafka_topic = 'speaker_queue'
app_kafka_key = 'speaker_requests'
app_group_id  = 'calculator'

app_web_host = 'http://face_storage:12350'
app_file_interface = '/get_speaker_file'

call_interval  = 1
sleep_interval = 7