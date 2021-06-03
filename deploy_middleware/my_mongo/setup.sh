#!/bin/bash
mongo -u my_root -p my_123456 <<EOF
use face_recognition;
db.createUser({user:'xcy',pwd:'xcy123456',roles:[{role:'readWrite',db:'face_recognition'}]});
db.users.insertOne({'username':'xxxxxx@qq.com', 'password': 'xxxxxx123', 'permission': 'NORMAL'});
EOF