"""
Django settings for authentication project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

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
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'



############################################################
# TODO: make this smarter. (this is currently just the
#       OSX homebrew path to latest version of gpg2. see
#       `doc/BOOTSTRAPPING-macosx.md` in repo.)
GNUPG_BINARY = "/usr/local/Cellar/gnupg2/2.0.20/bin/gpg2"

GNUPG_PASSPHRASE = SECRET_KEY
# On initial setup, this will be used to populate the name & other info
# for the server's default authentication key.
GNUPG_IDENTITY_DEFAULTS = {
  'name_real': 'Authentication.io',
  'name_email': 'test@example.com',
  'expire_date': '2015-01-01',
  'passphrase': GNUPG_PASSPHRASE
}
# After initial setup (the script will tell you how to update this), this
# line change from None to the long GPG key identifier.
# i.e. GNUPG_IDENTITY = "4034E60AA7827C5DF21A89AAA993E7156E0E9923"
GNUPG_IDENTITY = None
