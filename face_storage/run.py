# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : run.py
# @Function : TODO

from app import app
from upload import upload_api

app.register_blueprint(upload_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12350)
