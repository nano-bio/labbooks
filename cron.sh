#!/bin/bash
cd /var/opt/labbooks/
source bin/activate
python manage.py process_tasks --duration 3550
deactivate
