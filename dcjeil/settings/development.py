from .base import *
from dcjeil.util import get_server_info_value, get_social_login_secret_key

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dcjeil_develop.sqlite3'),
    }
}


INSTALLED_APPS += [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount'
]


MIDDLEWARE += [
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'member.oauth.backends.SocialLoginBackend'
]

SITE_ID = 1

SECRET_KEYS = get_social_login_secret_key("secret_keys")

NAVER_CLIENT_ID = 'e4ZsoJAd0lfPVJQldldH'
NAVER_SECRET_KEY = SECRET_KEYS["NAVER_SECRET_KEY"]

KAKAO_CLIENT_ID = '67e7757fd4460f510db528b575e0fa0d'
KAKAO_SECRET_KEY = SECRET_KEYS["KAKAO_SECRET_KEY"]

GOOGLE_CLIENT_ID = '24302309163-58kin7d8rn88pb8tj8k07srg71cgg9fg.apps.googleusercontent.com'
GOOGLE_SECRET_KEY = SECRET_KEYS["GOOGLE_SECRET_KEY"]

FACEBOOK_CLIENT_ID = '330925454976805'
FACEBOOK_SECRET_KEY = SECRET_KEYS["FACEBOOK_SECRET_KEY"]