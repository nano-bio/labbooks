import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/var/opt/labbooks/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'labbooks.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
