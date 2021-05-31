"""
Django settings for the project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
env = environ.Env()

READ_DOT_ENV_FILE = True
if READ_DOT_ENV_FILE:
    ENV_ROOT_DIR = environ.Path(__file__) - 3
    env.read_env(str(ENV_ROOT_DIR.path(".env")))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "jop1!g_+tqprunn=)bdx#qlmtjk6&b6!c&kz(d8d#^7&z38)d="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", True))

ALLOWED_HOSTS = ["0.0.0.0", "localhost", "*"]

APPEND_SLASH = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "django_filters",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    # Our apps
    "entities.apps.EntityConfig",
    "variables.apps.VariableConfig",
    "plots.apps.PlotsConfig",
    "activities.apps.ActivitiesConfig",
    "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# REST API Settings

DEFAULT_RENDERER_CLASSES = (
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    # filter backend
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # Authentication settings
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    # Swagger Documentation
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

if os.environ.get("POSTGRES_DB_NAME"):
    DATABASES["default"].update(
        {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("POSTGRES_DB_NAME"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_PORT_5432_TCP_ADDR"),
            "PORT": os.environ.get("POSTGRES_PORT_5432_TCP_PORT"),
        }
    )


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = "/static/"

# Collect static won't work if you haven't configured this
# django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set
#  the STATIC_ROOT setting to a filesystem path.
STATIC_ROOT = "/static/"

# Indicate that we're being executed by uWSGI
# This settings is used in urls.py to serve the static from within uWSGI
IS_WSGI = bool(os.environ.get("IS_WSGI", False))

# Setup support for proxy headers
# https://design.canonical.com/2015/08/django-behind-a-proxy-fixing-absolute-urls
# http://stackoverflow.com/questions/19669376/django-rest-framework-absolute-urls-with-nginx-always-return-127-0-0-1
# http://stackoverflow.com/questions/26435272/how-to-use-django-sslify-to-force-https-on-my-djangonginxgunicorn-web-app-and
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

# Django CORS
# see: https://pypi.org/project/django-cors-headers/
CORS_ALLOW_ALL_ORIGINS = True

# Spectacular Swagger documentation settings
SPECTACULAR_SETTINGS = {
    "TITLE": "OpenFisca-DjangoAPI Documentation",
    "DESCRIPTION": """A database and Django webserver layer for serving OpenFisca rulesets.\n
What does it do?
- ingests a OpenFisca ruleset into a SQL database, allowing for efficient/complex queries
- provides useful Restful endpoints for frontend services to query ruleset relations

Who should use this?
- teams who want to interrogate the <em>realtionship</em> between Variables in an OpenFisca ruleset
- teams who want to serve data to a frontend app from a generalised backend API

""",
    "TOS": None,
    "CONTACT": {
        "name": "NSW Government - Department of Industry Planning and Environment",
        "url": "https://github.com/energy-savings-scheme",
    },
    "LICENSE": {
        "name": "Licensed under the MIT License",
        "url": "https://github.com/RamParameswaran/openfisca-djangoapi/blob/main/LICENSE",
    },
}

###########################################
###########################################
###########################################

# OpenFisca settings
OPENFISCA_API_URL = env.str("OPENFISCA_API_URL", default="http://localhost:8001")
