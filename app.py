# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : app.py
# @Function : TODO

from flask import Flask
from flask_pymongo import PyMongo

import configs

def create_app():
    app = Flask(__name__)
    app.secret_key           = configs.app_secret_key
    app.config['MONGO_URI']  = configs.app_mongo_uri

    mongo = PyMongo(app=app)
    return app, mongo

app, mongo = create_app()
