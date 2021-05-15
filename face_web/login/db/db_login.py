from app import app, db
from login.app.permission import Permission

def get_user_info_from_user_id(user_id):
    user = db.users.find_one({'username': user_id})
    return user

def verify_login(username, password):
    user = db.users.find_one({'username': username, 'password': password})
    if not user:
        return False
    return True

def add_new_user(new_user):
    if db.users.find_one({'username': new_user['username']}):
        return -1
    return db.users.insert_one(new_user)


def get_user_permission_from_user_id(user_id):
    user = db.users.find_one({'username': user_id})
    permission = Permission.load_permission(user['permission'])
    app.logger.debug("[LOGIN][GET_PERMISSION] OK, username: {}, permission: {}".format(user_id, permission))
    return permission