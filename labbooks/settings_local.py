from labbooks.settings import *

ALLOWED_HOSTS = ['*']

DEBUG = True

# local ROOT pw mysql: fd7483jer9w3glSD%$w45ghdsZT
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'labbooks',
#         'USER': 'labbooks',
#         'PASSWORD': 'labbooks',
#         'HOST': '',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SURFTOF_BIGSHARE_DATA_ROOT = "Z:/Experiments/SurfTOF/Measurements/rawDATA/"
