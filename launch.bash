#!/bin/bash

if [[ $1 == "delete" ]]; then
  sudo docker image rm flask-server:v1
fi

sudo docker image inspect flask-server:v1 >/dev/null 2>&1
[[ $? != 0 ]] && echo "Image does not exist; building image" && sudo docker build -t flask-server:v1 .

sudo docker-compose up

# on exiting, check whether command failed or Ctrl-C was sent

# bad solution since ctrl-c triggers this
#if [ ! -z $? ]; then
#  sudo systemctl stop postgresql
#  sudo docker-compose up
#fi