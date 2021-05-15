from app import app

class Permission:
    NORMAL = 'NORMAL'
    ADMINISTER = 'ADMINISTER'
    MEMBER     = 'MEMBER'

    @staticmethod
    def load_permission(permission_str):
        if permission_str == Permission.NORMAL:
            return Permission.NORMAL
        if permission_str == Permission.ADMINISTER:
            return Permission.ADMINISTER
        if permission_str == Permission.MEMBER:
            return Permission.MEMBER
        app.logger.error("未识别的权限：{}".format(permission_str))
        # raise RuntimeError("未识别的权限：{}".format(permission_str))
        return Permission.NORMAL