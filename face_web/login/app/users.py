from login.db import db_login
from login.app.permission import Permission
import flask_login


class User(flask_login.UserMixin):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.permission = 'NORMAL'

    def is_visitor(self):
        try:
            return db_login.user_is_visitor(self.get_id())
        except Exception as e:
            return False

    def is_apiuser(self):
        try:
            user_permission = db_login.get_user_permission_from_user_id(self.get_id())
            return user_permission == Permission.APIUSER
        except:
            return False

    def is_admin(self):
        try:
            user_permission = db_login.get_user_permission_from_user_id(self.get_id())
            return user_permission == Permission.ADMINISTER
        except:
            return False
    def is_normal(self):
        try:
            user_permission = db_login.get_user_permission_from_user_id(self.get_id())
            return user_permission == Permission.NORMAL
        except:
            return False
    def is_member(self):
        try:
            user_permission = db_login.get_user_permission_from_user_id(self.get_id())
            return user_permission == Permission.MEMBER
        except:
            return False

    def upper_member(self):
        try:
            user_permission = db_login.get_user_permission_from_user_id(self.get_id())
            return user_permission == Permission.MEMBER or user_permission == Permission.ADMINISTER
        except:
            return False


