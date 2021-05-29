nohup python -u service.py >> service.log 2>&1 &
nohup python -u error_service.py >> service.log 2>&1 &
tail -f service.log