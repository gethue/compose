#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]
then
  brew install python3 openssl mysql redis
  pip3 install virtualenv
  virtualenv -p python3 python_env
  source python_env/bin/activate
  export LDFLAGS=-L/usr/local/opt/openssl/lib && export CPPFLAGS=-I/usr/local/opt/openssl/include
  pip3 install -r webapp/requirements.txt
else
  sudo apt-get update

  sudo apt-get install mysql-server -y
  sudo apt-get install python3-pip -y
  sudo apt-get install libmysqlclient-dev -y
  sudo apt-get install redis-server -y
  sudo apt-get install python3.8-venv
  # sudo apt-get install docker.io -y

  sudo pip3 install virtualenv
  python3.8 -m venv python_env

  source python_env/bin/activate

  pip3 install -r webapp/requirements.txt
fi
