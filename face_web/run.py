# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : run.py
# @Function : TODO

import view
from app import app
from login.app.web_login import login_print

app.register_blueprint(login_print)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12349, debug=True)
