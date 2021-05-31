# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : configs.py
# @Function : TODO

import flask_autoapi

face_detection_config = {
    'service_dir'               : './', # Service root directory
    'service_python_filename'   : 'predict',            # service2.py
    'service_python_interface'  : 'detect_face',            # service2 is the interface function

    'service_input_params' : {                           # interface input params are defined here
        'image_path': 'param1 describe here',
    },

    'service_output_params' : {                          # interface output params are defined here
        'result': 'result_path',
    },

    'deploy_mode'   : 'restful', # c++ deploy            # now only has restful deploy
    'deploy_port'   : '20001',                           # service port
    'service_route' : '/test_service'                    # service route
}

if __name__ == '__main__':
    flask_autoapi.launch(face_detection_config, host='0.0.0.0')