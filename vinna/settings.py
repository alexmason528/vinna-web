"""
Django settings for vinna project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import datetime
import stripe

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wx5(=7^kfbuzw7bxt7a9*72&3^kr4fjp)e6vfm*17+n$$26@h#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',

    'core.apps.CoreConfig',

    'server.notification',
    'server.media',
    'server.business',
    'server.purchase',
    'server.account',
    'server.member',
    'server.review',

    'client.client_home',
    'client.client_business',
    'client.client_member',

    'corsheaders'
]

MIDDLEWARE = [
    'vinna.middleware.disable_csrf_middleware',
#    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'vinna.middleware.basic_auth_middleware',
]



ROOT_URLCONF = 'vinna.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.realpath(os.path.dirname(__file__)) + '/templates/'
        ],
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

WSGI_APPLICATION = 'vinna.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'sql_mode': 'STRICT_ALL_TABLES',
            'init_command': 'SET default_storage_engine=INNODB',
        },
        'NAME': 'vinna_main','USER': 'root','PASSWORD': '','HOST': '127.0.0.1','PORT': '3306',
#        'NAME':'vinna_main','USER':'vinna','PASSWORD':'vinna123!','HOST':'cpvlabs.cwdkozsu0mvg.us-east-1.rds.amazonaws.com','PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.AllowAny',
    ],
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'vinna.authentication.CustomJSONWebTokenAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),

}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'vinna.utils.encode_handler',

    'JWT_DECODE_HANDLER':
    'vinna.utils.decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'vinna.utils.payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'vinna.utils.response_payload_handler',

    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,
}

PREPEND_WWW = False
ALLOWED_HOSTS = ['www.test.vinna.me','test.vinna.me','www.dev.vinna.me','dev.vinna.me','vinna.me','www.vinna.me','www.localhost','localhost']
APPEND_SLASH = True

#ROOT_URLCONF = 'myproject.urls.account'

# A dictionary of urlconf module paths, keyed by their subdomain.
#SUBDOMAIN_URLCONFS = {
#    None: 'myproject.urls.frontend',  # no subdomain, e.g. ``example.com``
#    'www': 'myproject.urls.frontend',
#    'api': 'myproject.urls.api',
#}


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "s"),
]

FORMAT_MODULE_PATH = [
]

BASICAUTH_USERNAME = 'vinna'
BASICAUTH_PASSWORD = 'vinnatesting123!'


EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAIHDE62KJU3KHNRNQ'
EMAIL_HOST_PASSWORD = 'AkIUtnqmwXQQCMnsGnXvBT3CS/MLlOQmIfkG5Rv13rcc'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
#EMAIL_USE_SSL = True
#EMAIL_PORT = 465

STRIPE_API_KEY = 'sk_test_RWKnLTTuJgU5Tzc3Gltv5zzH'
STRIPE_PUBLIC_KEY = 'pk_test_vSXaN8PlxDIA9SRDrvPyNllu'

CORS_ORIGIN_ALLOW_ALL = True