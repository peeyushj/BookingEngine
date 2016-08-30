"""
Django settings for booking_engine project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u#vl@00+z$i=)k_@#*0bu(5j-u(d*bw7c^kwsey(6px7m#8l#a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

LOGIN_URL = '/login'

LOGIN_REDIRECT_URL = '/account_info'

LOGOUT_URL = '/logout'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'booking_engine',
    'tokenapi',
    # 'tastypie',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'proxy_server.middleware.DisableCSRF',
)

# PROXY_API_KEYS = ['^ugfp@+cw!+se1b8kw%!23(sbrzk8f!uzrhqp$s)@67g9f1tdj', 'http://127.0.0.1:8001/']

# Write the route to the service you wish to use as token validation.
# If you don't wish to have a token validation, skip this setting
#PROXY_TOKEN_VALIDATION_SERVICE = 'project.services.token_service'

# The IP or domain address of the backend services to be consumed
BACKEND_HOST = 'localhost'

# The port through which the backend services will be consumed
BACKEND_PORT = '8001'

ROOT_URLCONF = 'server_setting.urls'

WSGI_APPLICATION = 'server_setting.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'booking_engine',                      # Or path to database file if using sqlite3.
#         'USER': 'root',                      # Not used with sqlite3.
#         'PASSWORD': 'root',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     },
#     'unit_selector': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'unit_selector',                      # Or path to database file if using sqlite3.
#         'USER': 'cfx_user',                      # Not used with sqlite3.
#         'PASSWORD': 'cfx_user@123',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '', 
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'booking_engine',                      # Or path to database file if using sqlite3.
        'USER': 'cf_stageuser',                      # Not used with sqlite3.
        'PASSWORD': 'CfSt@ge123',                  # Not used with sqlite3.
        'HOST': 'stagedb.cfteam.in',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'unit_selector': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'unit_selector',                      # Or path to database file if using sqlite3.
        'USER': 'cfx_user',                      # Not used with sqlite3.
        'PASSWORD': 'cfx_user@123',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', 
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'localhost:11211',
        'TIMEOUT': 60*60*24*7*4, #4 weeks
        'OPTIONS': {
            'MAX_ENTRIES': 10000
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'booking_engine/static')

STATIC_URL = '/static/'

DYLD_LIBRARY_PATH='/usr/local/mysql/lib/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static", "templates"),
)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATICFILES_DIRS = (
    BASE_DIR + '/static/',
)

AUTHENTICATION_BACKENDS = (
    "booking_engine.emailauth.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    "tokenapi.backends.TokenBackend",
    # "proxy_server.authentication.auth.ProxyServerBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

#For testing
PAYU_INFO = {'merchant_key': "gtKFFx",
             'merchant_salt': "eCwWELxi",
             # for production environment use 'https://secure.payu.in/_payment'
             'payment_url': 'https://test.payu.in/merchant/postservice.php?form=2',
}

#For Production
# PAYU_INFO = {'merchant_key': "ZpX1cg",
#              'merchant_salt': "xI1FwuZf",
#              # for production environment use 'https://secure.payu.in/_payment'
#              'payment_url': 'https://secure.payu.in/_payment',
# }

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'dealsmart'
EMAIL_HOST_PASSWORD = 'dealsmart@123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'online-booking@commonfloor.com'

TOKEN_TIMEOUT_DAYS = 1000

# REST_FRAMEWORK_SUPPORT = False
