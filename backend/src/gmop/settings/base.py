import os
import sys
import environ
import re

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hwn-lxq!d%ou7ob7hw@6e!+h1*d_!2mhqb=@s1@s2*5pqt_dj*'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    "cid.apps.CidAppConfig",
    'gmop.core',
    'gmop.users',
    'gmop.authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "cid.middleware.CidMiddleware",
    'gmop.core.middleware.LogRequestMiddleware',
]

ROOT_URLCONF = 'gmop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'gmop.wsgi.application'

DATABASES = {'default': {'NAME': 'gmop', 'USER': 'root', 'PASSWORD': 'example', 'HOST': 'mysql', 'PORT': 3306, 'ENGINE': 'django.db.backends.mysql'}}
# # DATABASES = {"default": env.db()}
# if 'test' in sys.argv or 'test_coverage' in sys.argv:
#     DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
#     DATABASES['default']['HOST'] = 'mysql'

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


LANGUAGE_CODE = 'en-us'

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        'Basic': {'type': 'basic'},
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
    "DEFAULT_AUTO_SCHEMA_CLASS": "gmop.core.swagger.ErrorResponseAutoSchema",
}

TIME_ZONE = 'UTC'

HOSTNAME = re.sub(
    r"^http(s)?://", "", env("SAML_HOST", default=env("HOSTNAME", default=""))
)

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

AUTH_USER_MODEL = "users.User"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "gmop.authentication.backends.SSOAuthBackend",
        "rest_framework.authentication.BasicAuthentication",
    ),
}

SAML2_AUTH = {
    "ATTRIBUTES_MAP": {"email": "email", "username": "givenName"},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
