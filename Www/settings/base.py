"""
    Django
"""

import os
import json
import environ
from Www.core.settings import Settings


class BaseSettings(Settings):
    """ Community base settings, don't use this directly. """

    SITE_ROOT = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    env = environ.Env(
        DEBUG=(bool, False),
        SECRET_KEY=str,
        INTERNAL_IPS=(list, ['127.0.0.1']),
        ALLOWED_HOSTS=(list, ['127.0.0.1']),
        # DB & Cache
        DATABASE_URL=str,
        REDIS_SERVER=(str, None),
        CACHE_PREFIX=(str, ""),
        CACHE_TIMEOUT=(int, 30),
        # EMAIL
        EMAIL_URL=str,
        DEFAULT_FROM_EMAIL=str,
        # AWS
        ENABLE_REMOTE_STORAGE=(bool, False),
        AWS_ACCESS_KEY_ID=str,
        AWS_SECRET_ACCESS_KEY=str,
        AWS_STORAGE_BUCKET_NAME=str,
    )

    env_path = None
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'Www.settings.dev':
        env_path = os.path.join(SITE_ROOT, '.config_project/environ/dev/.env')
    elif os.environ['DJANGO_SETTINGS_MODULE'] == 'Www.settings.production':
        env_path = os.path.join(SITE_ROOT, '.config_project/environ/production/.env')

    environ.Env.read_env(env_path)

    AUTH_USER_MODEL = 'custom_user.User'
    LOGIN_REDIRECT_URL = '/home/'

    # Debug settings
    DEBUG = env('DEBUG')
    SECRET_KEY = env('SECRET_KEY')
    ALLOWED_HOSTS = env('ALLOWED_HOSTS')
    INTERNAL_IPS = env('INTERNAL_IPS')
    WSGI_APPLICATION = 'Www.core.wsgi.application'
    ROOT_URLCONF = 'Www.core.urls'
    SITE_ID = 1
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LANGUAGES = (
        # info: https://docs.djangoproject.com/en/4.0/ref/settings/#globalization-i18n-l10n
        (LANGUAGE_CODE, 'English'),
    )

    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
    ]

    PROJECT_APPS = [
        'Www.apps.blog',
        'Www.apps.custom_user',
        'Www.apps.theme',
    ]

    THIRD_PARTY_APPS = [
        'widget_tweaks',
        #'debug_toolbar',
        'allauth',
        'meta',
        'ckeditor',
        'ckeditor_uploader',
        'tailwind',
    ]

    INSTALLED_APPS = PROJECT_APPS + DJANGO_APPS + THIRD_PARTY_APPS

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [SITE_ROOT+"/templates"],
            # 'APP_DIRS': True,
            'OPTIONS': {
                'debug': DEBUG,
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
            },
        },
    ]

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

    @property
    def DATABASES(self):  # noqa
        db_engine = self.env('DB_ENGINE')
        if db_engine == 'mysql':
            return {
                'default': self.env.db()
            }
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(self.SITE_ROOT, 'dev.db'),
            }
        }

    @property
    def CACHES(self):
        if self.env('REDIS_SERVER'):
            return {
                "default": {
                    "BACKEND": "django_redis.cache.RedisCache",
                    'PREFIX': self.env('CACHE_PREFIX'),
                    'TIMEOUT': self.env('CACHE_TIMEOUT'),
                    "LOCATION": self.env('REDIS_SERVER'),
                    "OPTIONS": {
                        "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    }
                }
            }
        else:
            return  {
                'default': {
                    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
                }
            }

    FIXTURE_DIRS = [os.path.join(SITE_ROOT, '.config_project/fixtures')]  # No debe cambiar el path de este dir

    # Media
    if env('ENABLE_REMOTE_STORAGE'):
        AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

        AWS_S3_CUSTOM_DOMAIN = F'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
        MEDIAFILES_LOCATION = 'media'
        MEDIA_URL = F"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"
        DEFAULT_FILE_STORAGE = 'Www.core.storages.CustomMediaStorage'

        AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
        }
    else:
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(SITE_ROOT, '.media')

    # Static
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(SITE_ROOT, '.static')
    # STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
    STATICFILES_DIRS = [
        os.path.join(SITE_ROOT, 'Www/static'),
        os.path.join(SITE_ROOT, 'Www/apps/custom_user/static'),
    ]

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
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    LOGS_ROOT = os.path.join(SITE_ROOT, '.logs')
    LOG_FORMAT = '|| %(levelname)s || %(name)s || %(lineno)s[%(process)d] || %(message)s'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': LOG_FORMAT,
                'datefmt': '%d/%b/%Y %H:%M:%S',
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
        },
        'handlers': {
            'console': {
                'level': env('LOG_CONSOLE_LEVEL'),
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'debug': {
                'level': env('LOG_FILE_DJANGO_LEVEL'),
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOGS_ROOT, 'django/debug.log'),
                'formatter': 'default',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'formatter': 'default',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
            'null': {
                'class': 'logging.NullHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['debug', 'console', 'mail_admins'],
                'level': 'DEBUG',
            },
            'django': {
                'handlers': ['debug', 'console', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'mafuyu': {
                'handlers': ['debug', 'console', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.security.DisallowedHost': {
                'handlers': ['null'],
                'propagate': False,
            },
        },
    }

    # CKEDITOR
    CKEDITOR_UPLOAD_PATH = "uploads/"
    CKEDITOR_IMAGE_BACKEND = "pillow"
    CKEDITOR_RESTRICT_BY_USER = True
    # Tailwind
    TAILWIND_APP_NAME = 'Www.apps.theme'