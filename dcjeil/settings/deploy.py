from .base import *
from dcjeil.util import get_server_info_value


SETTING_PRD_DIC = get_server_info_value("production")

DEBUG = False

SECRET_KEY = SETTING_PRD_DIC["SECRET_KEY"]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': SETTING_PRD_DIC['DATABASES']["default"]
}

FILE_UPLOAD_MAX_MEMORY_SIZE = 200000000