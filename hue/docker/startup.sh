#!/bin/bash

python3 manage.py migrate --noinput

gunicorn hue.wsgi --bind 0.0.0.0:8000 --threads 10 --access-logfile '-' --error-logfile '-'
