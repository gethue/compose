#!/bin/bash

python compose/manage.py migrate --noinput

gunicorn core.wsgi --pythonpath compose --bind 0.0.0.0:8005 --threads 10 --access-logfile '-' --error-logfile '-'
