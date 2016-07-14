"""
Django settings for JABRIL project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
#from campaign.models import User

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kts+d%(k4wh7pag%g2ss4^_cb31#%5w6)9x%w!+9#ky=91px@%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #True

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'campaign',
    'markdown_deux',
    'analytical',
    'easy_thumbnails',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'JABRIL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'campaign.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'JABRIL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
#POSTGRES
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'hello',
#        'USER': 'hello_django',
#        'PASSWORD': '0615538193',
#        'HOST': 'localhost',
#        'PORT': '',                      # Set to empty string for default.
#    }
#}

#MARIADB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hello',
        'USER': 'halqaran_django',
        'PASSWORD': 'cudurdilaadhimo',
        'HOST': 'localhost',
        'PORT': '',
    }
}
'''


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') # for pythonanywhere only '/home/jabril/JABRIL' #os.path.join(BASE_DIR, 'static')


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home2/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # for pythonanywhere '/home/jabril/JABRIL/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'


######################################################
# MARKDOWN SETTINGS STARTS HERE
######################################################
from markdown_deux.conf.settings import MARKDOWN_DEUX_DEFAULT_STYLE

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": "escape",
    },
}
# MARKDOWN SETTINGS END HERE
#######################################################

############### THUMPNAILS APP ########################
THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (100, 100), 'crop': True},
    },
}

#######################  SITE VARIABLES ###################
SITE_DOMAIN = 'li1487-184.members.linode.com'
SITE_NAME = {"so":"Hal Qaran", "en":"Hal Qaran"}
SITE_MOTO = {"so":"Horumar iyo Hal Qaran baan Rabnaa!", "en":"We need development and Hal Qaran"}
SITE_DESCRIPTION = {"so":"Bogga Rasmiga ah ee Hal Qaran", "en":"The official page for Hal Qaran Movement (HQM)."}

#GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-80178068-1'
CLICKY_SITE_ID = '100971100'

############## EMAIL VARIABLES ###############
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'halqaraninfocenter@gmail.com'
EMAIL_HOST_PASSWORD = 'hic/sharaf.143'
DEFAULT_FROM_EMAIL = 'halqaraninfocenter@gmail.com'
DEFAULT_TO_EMAIL = 'boolow5@gmail.com'

############# CUSTOM MESSAGES SETTINGS ##############
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',
                }
