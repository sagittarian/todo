import os.path

from passwords import *

BASEDIR = os.path.dirname(os.path.dirname(__file__))
APPDIR = os.path.dirname(BASEDIR)

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'todo',
        'USER': 'todo_user',
        'PASSWORD': DBPASSWORD,
        'HOST': '',
        'PORT': '',
    }
}

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(APPDIR, 'todo_frontend')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/'

ROOT_URLCONF = 'todo.urls'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'mesha'

