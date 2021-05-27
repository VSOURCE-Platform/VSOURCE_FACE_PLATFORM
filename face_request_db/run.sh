nohup python -u face_service.py >> request.log 2>&1 &
nohup python -u speaker_service.py >> request.log 2>&1 &
tail -f request.log