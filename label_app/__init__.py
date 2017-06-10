from django.apps import AppConfig
import os

VERBOSE_APP_NAME = '标注管理'


def get_current_app_name(file):
    return os.path.dirname(file).replace('\\', '/').split('/')[-1]


class AppVerboseNameConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME

default_app_config = get_current_app_name(__file__) + '.__init__.AppVerboseNameConfig'