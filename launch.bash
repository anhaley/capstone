#!/bin/bash

sudo docker image inspect flask-server:v1 >/dev/null 2>&1
[[ $? != 0 ]] && echo "Image does not exist; building image" && sudo docker build -t flask-server:v1 .

sudo docker-compose up
if [ ! -z $? ]; then
  sudo systemctl stop postgresql
  sudo docker-compose up
fi