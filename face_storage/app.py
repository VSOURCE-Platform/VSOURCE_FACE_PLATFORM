# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : app.py
# @Function : TODO

from flask import Flask

import configs


def create_app():
    app = Flask(__name__)
    app.secret_key           = configs.app_secret_key
    app.config['UPLOAD_FOLDER']     = configs.uploader_folder
    return app

app = create_app()
