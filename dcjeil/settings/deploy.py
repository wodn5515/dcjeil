from .base import *
from dcjeil.util import get_server_info_value


SETTING_PRD_DIC = get_server_info_value("production")

DEBUG = False

SECRET_KEY = SETTING_PRD_DIC["SECRET_KEY"]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': SETTING_PRD_DIC['DATABASES']["default"]
}