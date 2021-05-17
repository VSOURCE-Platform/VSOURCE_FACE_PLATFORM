# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : app.py
# @Function : TODO

from flask import Flask
from flask_login import LoginManager
import pymongo

import configs


from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    app.secret_key           = configs.app_secret_key

    client = pymongo.MongoClient(host=configs.app_database_host, port=configs.app_database_port)
    db = client[configs.app_database_name]
    auth_ans = db.authenticate(name=configs.app_database_user, password=configs.app_database_pwd)
    return app, db

app, db = create_app()
CORS(app, supports_credentials=True, resources=r'/*')
login_manager = LoginManager(app)
