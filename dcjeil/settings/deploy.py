from .base import *
from dcjeil.utils import get_server_info_value

SETTING_PRD_DIC = get_server_info_value("production")

DEBUG = False

SECRET_KEY = SETTING_PRD_DIC["SECRET_KEY"]

ALLOWED_HOSTS = [
    '13.209.219.30',
    'dcjeil.net',
    'www.dcjeil.net'
    ]

DATABASES = {
    'default': SETTING_PRD_DIC['DATABASES']["default"]
}

AWS_ACCESS_KEY_ID = SETTING_PRD_DIC["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = SETTING_PRD_DIC["AWS_SECRET_ACCESS_KEY"]

FILE_UPLOAD_MAX_MEMORY_SIZE = 200000000
