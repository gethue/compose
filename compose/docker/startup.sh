#!/bin/bash

python compose/manage.py migrate --noinput

# Temp demo DB to query
DJANGO_SUPERUSER_PASSWORD=hue python compose/manage.py createsuperuser --username hue --noinput --email 'hue@gethue.com'
cp compose/db.sqlite3 compose/db-demo.sqlite3

gunicorn compose.core.wsgi --bind 0.0.0.0:8005 --threads 10 --access-logfile '-' --error-logfile '-'
