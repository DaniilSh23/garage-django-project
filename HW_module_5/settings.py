"""
Django settings for HW_module_5 project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import django.core.cache.backends.locmem

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5dhm-33ocrp#an__ua1$qyk1+82_gkwk4pnb6nr4leatdfibke'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',  # это для карты сайта
    'django.contrib.sites',       # это для карты сайта
    'news.apps.NewsConfig',
    'app_users',
    'app_media.apps.AppMediaConfig',
    'rest_framework',
    'drf_taste',
    'book_library',
    'django_filters',   # приложение для фильтрации
    'drf_yasg',
    'app_blogs',
    'debug_toolbar',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'HW_module_5.urls'

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
            ],
        },
    },
]

# определяем тип кэширования в Джанго(берём из имеющихся)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

WSGI_APPLICATION = 'HW_module_5.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('de', 'Deutsche'),
    ('es', 'El español'),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'),]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# перенаправление по заданному адресу при логине
LOGIN_REDIRECT_URL = '/'

# перенаправление по заданному адресу при логауте
# (может также быть реализовано во вьюхе)
LOGOUT_REDIRECT_URL = '/'

# время жизни сессии (указывается в секундах, здесь задано 30 дней)
SESSION_COOKIE_AGE = 30 * 24 * 60 * 60

SESSION_COOKIE_NAME = 'sessionid'

# закрытие сессии при закрытии браузера, я поставил Тру, по умолчанию Фолс
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# путь для сохранения файлов, в этом случае:
# корень проекта(значение параметра BASE_DIR, указанном выше в этом коде + 'media/',
# таким образом все файлы будут попадать в папку media корня проекта
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    # это глобальный выбор пагинатора
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # размер страницы, на странице будут отображаться 2 записи из БД
    'PAGE_SIZE': 10,
    # глобальная настройка фильтрации по умолчанию
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
        'propagate': True,
    },
}

INTERNAL_IPS = [
    '127.0.0.1',
]
