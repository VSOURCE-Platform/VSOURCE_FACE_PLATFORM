# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : pages.py
# @Function : TODO

import flask
import flask_login

from login import login_required_and_redirect

page_print = flask.Blueprint('page', __name__, template_folder='./templates', static_folder='./static')

@page_print.route('/', methods=['GET'])
def index_page():
    return flask.render_template('index.html')

@page_print.route('/login_page', methods=['GET'])
def login_page():
    return flask.render_template('login.html')

#
# @page_print.route('/face', methods=['GET'])
# def main_page():
#     return flask.render_template('main.html')

@page_print.route('/face_dashboard', methods=['GET'])
@login_required_and_redirect
def face_dashboard_page():
    return flask.render_template('face_dashboard.html')

@page_print.route('/submit_page')
@flask_login.login_required
def submit_page():
    return flask.render_template('submit_page.html')

@page_print.route('/favicon.ico')
def get_favicon():
    return flask.current_app.send_static_file('favicon.ico')