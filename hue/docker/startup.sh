#!/bin/bash

python3 manage.py migrate --noinput

gunicorn core.wsgi --bind 0.0.0.0:8005 --threads 10 --access-logfile '-' --error-logfile '-'
