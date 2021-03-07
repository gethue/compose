#!/bin/bash

compose migrate

# Temp hue:hue and demo DB
DJANGO_SUPERUSER_PASSWORD=hue compose createsuperuser --username hue --noinput --email 'hue@gethue.com'
cp /usr/local/lib/python3.8/site-packages/compose/db.sqlite3 db-demo.sqlite3

compose start
