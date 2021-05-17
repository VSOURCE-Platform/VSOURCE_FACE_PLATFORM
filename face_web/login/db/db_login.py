import time
from app import app, db
from login.app.permission import Permission

def get_user_info_from_user_id(user_id):
    user = db.users.find_one({'username': user_id})
    if not user:
        # 从visitor里找一下
        user = db.visitor_users.find_one({'username': user_id})
        user['permission'] = 'VISITOR'
    return user

def user_is_visitor(user_id):
    user = db.visitor_users.find_one({'username': user_id})
    if not user:
        return False
    return True

def verify_login(username, password):
    user = db.users.find_one({'username': username, 'password': password})
    if not user:
        return False
    return True

def add_new_user(new_user):
    if db.users.find_one({'username': new_user['username']}):
        return -1
    return db.users.insert_one(new_user)

def add_visitor_user(username):
    visitor_item = {
        'username': username,
        'create_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    return db.visitor_users.insert_one(visitor_item)


def get_user_permission_from_user_id(user_id):
    user = db.users.find_one({'username': user_id})
    permission = Permission.load_permission(user['permission'])
    app.logger.debug("[LOGIN][GET_PERMISSION] OK, username: {}, permission: {}".format(user_id, permission))
    return permission