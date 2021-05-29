# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : web_login.py
# @Function : TODO

import uuid
import threading

import flask
import flask_login

from flask import request, Blueprint
from flask_cors import cross_origin

from app import app
from login import user_instance
from login.db import db_login
import configs

login_print = Blueprint('login', __name__, template_folder='../templates', static_folder='../static', static_url_path='/login')

@login_print.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        if not db_login.verify_login(username=username, password=password):
            app.logger.error("{} 登录失败".format(username))
            rsp = flask.jsonify({'status': 400, 'message': "Not Valid"})
            return rsp
        lock = threading.RLock()
        lock.acquire()
        user_instance.id = username
        user_instance.permission = db_login.get_user_permission_from_user_id(username)
        flask_login.login_user(user_instance)
        lock.release()
        app.logger.info("{}({}) 登录成功".format(username, db_login.get_user_permission_from_user_id(username)))
        rsp = flask.jsonify({'status': 200, 'message': "OK"})
        return rsp

@login_print.route('/login_as_visitor', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def login_as_visitor():
    if request.method == "POST":
        tmp_user_id = 'VISITOR_' + str(uuid.uuid1())
        lock = threading.RLock()
        lock.acquire()
        user_instance.id = tmp_user_id
        user_instance.permission = 'VISITOR'
        flask_login.login_user(user_instance, duration=configs.visitor_expire_time)
        db_login.add_visitor_user(tmp_user_id)
        lock.release()
        app.logger.info("{}({}) 登录成功".format(tmp_user_id, 'as a visitor.'))
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

@login_print.route('/now_user', methods=['GET'])
# @flask_login.login_required
def now_user():
    service_status = 'Active'
    if not flask_login.current_user.is_authenticated:
        # 未登录
        service_status = 'Logout'
        return flask.jsonify({'status': 200,
                              'username': '未登录用户',
                              'user_permission': 'NONE',
                              'service_status': service_status})
    if flask_login.current_user.is_visitor():
        if flask_login.current_user.is_visitor():
            service_status = 'No Permission (visitor user)'
        return flask.jsonify({'status': 200,
                              'username': str(flask_login.current_user.id)[:15],
                              'user_permission': str(flask_login.current_user.permission),
                              'service_status': service_status})
    return flask.jsonify({'status': 200,
                          'username': str(flask_login.current_user.id),
                          'user_permission': str(flask_login.current_user.permission),
                          'service_status': service_status})