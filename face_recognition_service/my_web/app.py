# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : app.py
# @Function : TODO

from flask import Flask
import pymongo

import configs


def create_app():
    app = Flask(__name__)
    app.secret_key           = configs.app_secret_key

    client = pymongo.MongoClient(host=configs.app_database_host, port=configs.app_database_port)
    db = client[configs.app_database_name]
    return app, db

app, db = create_app()
