#!/bin/sh
cd ..
git pull
cd dockerfile
echo -e "\033[36m Git pull finished. \033[0m"
# Stop and Delete all containers
docker-compose stop
docker-compose rm <<EOF
Y
EOF

echo -e "\033[36m All containers have been stopped and removed. \033[0m"

# Delete Images
if [ $1 -eq "with_db" ];
then
  docker rmi dockerfile_result_service
  docker rmi dockerfile_fr_service
  docker rmi dockerfile_my_web
  docker rmi dockerfile_my_mongo
  docker rmi dockerfile_my_redis
else
  docker rmi dockerfile_result_service
  docker rmi dockerfile_fr_service
  docker rmi dockerfile_my_web
fi

echo -e "\033[36m Images have been deleted. \033[0m"
echo -e "\033[36m Rebuilding images and run containers... \033[0m"
docker-compose up -d
echo -e "\033[36m CI finished and everything seems successfully. \033[0m"


