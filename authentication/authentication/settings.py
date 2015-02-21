"""
Django settings for authentication project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# ONLY EDIT PROJECT DEFAULTS IN THIS FILE. IF YOU NEED TO CHANGE
# SOMETHING FOR YOUR SYSTEM, GO UP ONE DIRECTORY AND COPY
# "local_settings.py.example" INTO A "local_settings.py" FILE
# AND DO ALL YOUR CONFIGURATION THERE. (Settings in that file override
# ones in this one.)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-b(fl18((n58j#36nq3!n%!^h433)6plpop2g_@0)f7gdj#ku*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'django_yubico',
    'authentication.authapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# AUTHENTICATION_BACKENDS = (
#     'django_yubico.backends.YubicoBackend',
#     'django_yubico.backends.YubicoBackendRequireYubikey',
# )

ROOT_URLCONF = 'authentication.urls'

WSGI_APPLICATION = 'authentication.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# https://docs.djangoproject.com/en/1.7/howto/static-files/deployment/
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

# Media files (user uploads)
MEDIA_URL = '/documents/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'server_documents')

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL='/'

############################################################
# Default settings for Authentication

GNUPG_BINARY = None
GNUPG_PASSPHRASE = None
GNUPG_IDENTITY_DEFAULTS = {
    'name_real': 'Authentication Default Config',
    'name_email': 'authentication@localhost',
    'passphrase': GNUPG_PASSPHRASE
}
GNUPG_IDENTITY_ID = None

############################################################

if os.path.exists(os.path.join(BASE_DIR, 'local_settings.py')):
    from local_settings import *
