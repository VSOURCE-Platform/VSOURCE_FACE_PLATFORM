from login.db import db_login
from login.app.permission import Permission
import flask_login


class User(flask_login.UserMixin):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
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


