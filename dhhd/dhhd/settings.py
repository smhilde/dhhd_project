"""
Django settings for dhhd project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open('sk.txt') as f:
	SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['hildebrew.pythonanywhere.com', 'donhildebrandhomedesigns.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'plan',
	'store',
	'registration',
#	'endless_pagination',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dhhd.urls'

WSGI_APPLICATION = 'dhhd.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Tempates
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = [
	TEMPLATE_PATH,
	]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

STATICFILES_DIRS = (
	STATIC_PATH,
	)
	
REGISTRATION_OPEN = True       # If true, users can register.
ACCOUNT_ACTIVATION_DAYS = 7    # One-week activation window. You can use any value.
REGISTRATION_AUTO_LOGIN = True # If true, the newly registered user will be logged in.
LOGIN_REDIRECT_URL = '/'       # The page you want users to arrive at after they've successfully logged in.
LOGIN_URL = '/accounts/login/' # The page users are directed to if they are not logged in and try to access
                               # pages that require authentication.

# For Endless Pagination
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
	'django.core.context_processors.request',
	)
ENDLESS_PAGINATION_PER_PAGE = 9
ENDLESS_PAGINATION_ORPHANS = 2