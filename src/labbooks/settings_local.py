from labbooks.settings import *

ALLOWED_HOSTS = ['*']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SURFTOF_BIGSHARE_DATA_ROOT = "Z:/Experiments/SurfTOF/Measurements/rawDATA/"
SURFTOF_EXPORT_CPM_DIR = "surftof/cpm-export/"
TOFFY2_REPLACE_H5_PATH = ['', ""]

CLUSTOF_FILES_ROOT = 'clustofdata/'
NANOPARTICLES_DATA_ROOT = 'Z:/Software/labbooks/nanoparticles/testfiles/'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
