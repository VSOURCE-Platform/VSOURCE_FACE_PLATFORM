import flask
import flask_login
from functools import wraps

from app import app, login_manager
from login.db import db_login
from login.app.users import User

user_instance = User()

# 权限装饰器
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not flask_login.current_user.is_admin():
            flask.abort(403)
        return func(*args, **kwargs)
    return decorated_function

def member_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not flask_login.current_user.is_member() and not flask_login.current_user.is_admin():
            flask.abort(403)
        return func(*args, **kwargs)
    return decorated_function

def login_required_and_redirect(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not flask_login.current_user.is_authenticated:
            redirect_dict = {
                'face_dashboard_page': '/face_dashboard',
                'speaker_dashboard_page': '/speaker_dashboard',
                'face_detection_dashboard_page': '/face_detection_dashboard',
            }
            from_function = func.__name__
            if from_function in redirect_dict.keys():
                return flask.redirect(flask.url_for('page.login_page', pre_url=redirect_dict[func.__name__]))
            else:
                return flask.redirect('/login_page')
        return func(*args, **kwargs)
    return decorated_function

def upper_visitor(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not flask_login.current_user.is_authenticated:
            return flask.redirect('/login_page')
        if flask_login.current_user.is_visitor():
            return flask.redirect('/login_page')
        return func(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def user_loader(user_login_id):
    user = db_login.get_user_info_from_user_id(user_login_id)
    if not user:
        return
    user_instance.id = user_login_id
    return user_instance


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if db_login.verify_login(username=username, password=request.form.get('password')):
        user_instance.id = username
        return user_instance
    return


