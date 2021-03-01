#!/bin/bash

compose migrate

# Temp hue:hue and demo DB
DJANGO_SUPERUSER_PASSWORD=hue compose createsuperuser --username hue --noinput --email 'hue@gethue.com'
cp compose/db.sqlite3 compose/db-demo.sqlite3

compose start
