"""
Django settings for schruff project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from django.utils.translation import ugettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')y1h#qc#gtd2x-syzzg0@8xq6)hng2jbvnf6vh9q5lpv=d60wt'

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
    'order',
    'debug_toolbar',
    'ckeditor',
    'cookiebanner'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'schruff.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'order.context_processors.setting_enhancement',
            ],
        },
    },
]

WSGI_APPLICATION = 'schruff.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/order/'
LOGOUT_REDIRECT_URL = '/order/'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

COOKIEBANNER = {
    "title": _("Cookie settings"),
    "header_text": _("Diese Webseite nutzt Cookies. Einige davon sind f??r den ordnungsgem????en Betrieb der Webseite erforderlich. "
                     "Andere dienen lediglich statistischen Zwecken."),
    "footer_text": _("Bitte hier akzeptieren:"),
    "footer_links": [
        {
            "title": _("Impressum"),
            "href": "/order/impressum"
        },
        {
            "title": _("Datenschutz"),
            "href": "/order/datenschutz"
        },
    ],
    "groups": [
        {
            "id": "essential",
            "name": _("Notwendige Cookies"),
            "description": _("Diese sind f??r den Betrieb der Webseite technisch erforderlich."),
            "cookies": [
                {
                    "pattern": "cookiebanner",
                    "description": _("Damit dieses Fenster nach dem akzeptieren auch wieder verschwindet"),
                },
                {
                    "pattern": "csrftoken",
                    "description": _("Zum Schutz vor Cross-Site-Request-Forgery Angriffen."),
                },
                {
                    "pattern": "sessionid",
                    "description": _("Ohne dieses Cookie kann keine Bestellung durchgef??hrt werden."),
                },
            ],
        },
        {
            "id": "analytics",
            "name": _("Analytics"),
            "optional": True,
            "cookies": [
                {
                    "pattern": "_owa_.*",
                    "description": _("Open Web Analytics Cookies zur Website Analysis. Weitere Information in der Datenschutzerkl??rung"),
                },
            ],
        },
    ],
}

# This must be the last part of the settings file

try:
    from .local_settings import *
    print('There local settings')
except ImportError:
    print('There is no local settings, you must be on production')
