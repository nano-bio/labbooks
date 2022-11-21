#!/usr/bin/env bash

python manage.py migrate --noinput
#python manage.py crontab add

#service cron start

gunicorn labbooks.wsgi -b django:8000
