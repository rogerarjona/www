from __future__ import absolute_import
from .base import BaseSettings

from datetime import timedelta


class DevSettings(BaseSettings):

    @property
    def INSTALLED_APPS(self):
        installed_apps = list(BaseSettings.INSTALLED_APPS)
        installed_apps += [
            'debug_toolbar',
            'django_browser_reload',
        ]
        return installed_apps

    @property
    def MIDDLEWARE(self):
        middlewares = list(BaseSettings.MIDDLEWARE)
        middlewares.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        middlewares.insert(1, 'django_browser_reload.middleware.BrowserReloadMiddleware')
        return middlewares


DevSettings.load_settings(__name__)
