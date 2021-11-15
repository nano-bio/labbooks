import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# set the IP for CLUSTOF here
CLUSTOFIP = '138.232.74.13'

# set the IP for SNOWBALL here
SNOWBALLIP = '138.232.74.207'

# set IPS for all pressure writing devices here
# snowball, josis computer
PRESSUREIPS = ['138.232.74.145', '138.232.74.103', '138.232.74.207']


ADMINS = (
    ('FelixD', 'felix.duensing@uibk.ac.at'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'labbooks',
        'USER': 'labbooks',
        'PASSWORD': 'labbooks',
        'HOST': '',
        'PORT': '',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

ALLOWED_HOSTS = ['138.232.74.41', 'ideadb.uibk.ac.at']  # ideadb see clustof -> views

SITE_ID = 1

TIME_ZONE = 'Europe/Vienna'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = '/admin/login/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediaroot/')
MEDIA_URL = '/files/'

STATIC_URL = '/staticfiles/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i=d0pz8apxr+0!25lwozu)e$)q*^1k4x=494ga6xi-++67d_*&amp;'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'labbooks.urls'

WSGI_APPLICATION = 'labbooks.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'rest_framework',
    'crispy_forms',
    "crispy_bootstrap5",
    'ckeditor',

    'cheminventory',
    'journal',
    'labinventory',
    'massspectra',

    'clustof',
    'nanoparticles',
    'pulsetube',
    'surftof',
    'snowball',
    'toffy',
    'toffy2',
    'vg',
    'wippi',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
CLUSTOF_FILES_ROOT = '/var/storage/clustof/'
SURFTOF_BIGSHARE_DATA_ROOT = "/mnt/bigshare/Experiments/SurfTOF/Measurements/rawDATA/"
NANOPARTICLES_DATA_ROOT = "/mnt/bigshare/"
