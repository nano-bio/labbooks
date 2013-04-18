import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/var/opt/labbooks/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'labbooks.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
