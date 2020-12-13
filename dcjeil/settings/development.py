from .base import *
from dcjeil.util import get_server_info_value

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(SyuV>rp:hS7{JS`&80`G70gx]qdoaoB:!)vVD30Ph<AZJ#JkM'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dcjeil_local',
        'USER': 'root',
        'PASSWORD': 'local',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}


INSTALLED_APPS += [
]


MIDDLEWARE += [
]