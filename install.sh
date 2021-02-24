#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]
then
  brew install python3 mysql redis
  pip3 install virtualenv
  virtualenv -p python3 python_env
else
  sudo apt-get update

  sudo apt-get install mysql-server -y
  sudo apt-get install python3-pip -y
  sudo apt-get install libmysqlclient-dev -y
  sudo apt-get install redis-server -y
  sudo apt-get install python3.8-venv

  sudo pip3 install virtualenv
  python3.8 -m venv python_env
fi
