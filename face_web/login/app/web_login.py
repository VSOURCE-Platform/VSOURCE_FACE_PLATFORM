# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : web_login.py
# @Function : TODO

import flask
import flask_login

from flask import request, Blueprint
from flask_cors import cross_origin

from app import app
from login import user_instance
from login.db import db_login

login_print = Blueprint('login', __name__, template_folder='../templates', static_folder='../static', static_url_path='/login')

@login_print.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == "POST":
        # data = request.get_json(silent=True)
        # username = data['username']
        # password = data['password']
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        if not db_login.verify_login(username=username, password=password):
            app.logger.error("{} 登录失败".format(username))
            rsp = flask.jsonify({'status': 400, 'message': "Not Valid"})
            return rsp
        user_instance.id = username
        flask_login.login_user(user_instance)
        app.logger.info("{}({}) 登录成功".format(username, db_login.get_user_permission_from_user_id(username)))
        rsp = flask.jsonify({'status': 200, 'message': "OK"})
        return rsp

@login_print.route('/is_login', methods=['GET'])
@cross_origin(supports_credentials=True)
def islogin():
    if hasattr(flask_login.current_user, 'id'):
        return flask.jsonify({'status': 200, 'message': "OK"})
    return flask.jsonify({'status': 400, 'message': "NO"})

@login_print.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    new_user = {
        'username': username,
        'password': password,
        'permission': 'NORMAL'
    }
    try:
        add_result = db_login.add_new_user(new_user)
        if add_result == -1:
            return flask.jsonify({'status': 401, 'message': "repeat_username"})
        if add_result:
            return flask.jsonify({'status': 200, 'message': "OK"})
        return flask.jsonify({'status': 400, 'message': "Error."})
    except Exception as e:
        return flask.jsonify({'status': 400, 'message': "Error.", 'err_msg': str(e)})


@login_print.route('/logout')
@cross_origin(supports_credentials=True)
@flask_login.login_required
def logout():
    try:
        app.logger.info("{} 登出成功".format(flask_login.current_user.id))
        flask_login.logout_user()
        # return flask.jsonify({'status': 200, 'message': "OK"})
        return flask.redirect('/')
    except Exception as e:
        return flask.jsonify({'status': 400, 'message': "ERROR"})
