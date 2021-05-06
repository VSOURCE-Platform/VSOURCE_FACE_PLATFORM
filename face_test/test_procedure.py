# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : test_procedure.py
# @Function : TODO

import json
import time
import pymongo
import requests
import traceback

def test_v_1_0_4():
    try:
        face_service_params = {
            'face1': './work/face_recognition_native_api/tmp/0006_01.jpg',
            'face2': './work/face_recognition_native_api/tmp/0007_01.jpg'
        }
        face_service_url = 'http://127.0.0.1:12349/face_service'
        response = requests.get(face_service_url, params=face_service_params)
        service_reponse = json.loads(response.text)
        assert service_reponse['status'] == 200

        time.sleep(5)

        face_result_params = {
            'id': service_reponse['id']
        }
        face_result_url = 'http://127.0.0.1:12349/get_result'
        response = requests.get(face_result_url, params=face_result_params)
        result_response = json.loads(response.text)
        assert result_response['status'] == 200


        # db
        app_database_host = 'localhost'
        # 要注意，这里host要改，因为不在容器内调用
        app_database_name = 'face_recognition'
        app_database_user = 'xcy'
        app_database_pwd  = 'xcy123456'
        app_database_port = 27017

        app_database_table_name = 'face_list'
        app_database_request_table = 'face_requests'


        client = pymongo.MongoClient(host=app_database_host, port=app_database_port)
        db = client[app_database_name]
        db.authenticate(name=app_database_user, password=app_database_pwd)
        face_list_table = db[app_database_table_name]
        face_result_ans = face_list_table.find_one({'id': service_reponse['id']})
        print(face_result_ans)
        score = face_result_ans['score']
        print('score:', score)
        assert round(float(score), 4) == 1.0564

        request_table = db[app_database_request_table]
        request_info = request_table.find_one({'id': face_result_params['id']})
        print(request_info)
        assert request_info['status'] == 'finished'
        print('\033[36m Successful Tested! \033[0m')
        return {'status': 200}
    except Exception as e:
        traceback.print_exc()
        print('Tested Failed!')
        return {'status': 400}

if __name__ == '__main__':
    test_result = test_v_1_0_4()