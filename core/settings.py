"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


LOGGING_DIR = os.path.join(settings.BASE_DIR, 'logs') # added this 3 lines for logging
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(cf19d^*$o1&9aqrk3bbx_hwf7@k6aqjp%5nh5a(au_cj7b*#v'

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
    'rest_framework', 
    'authentication',
    'employee_management',
    "channels",
    'debug_toolbar', # added this for debugger
   
]

INTERNAL_IPS = [   # added did this for debugger
    "127.0.0.1",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authentication.middleware.JWTAuthenticationMiddleware', # added this for custom jwt auth class
    'debug_toolbar.middleware.DebugToolbarMiddleware', # added this line for debugger 
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'employee_management', 'templates')],
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


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'employee_management', 'static')  # Ensure static files are loaded
]

WSGI_APPLICATION = 'core.wsgi.application' # commented when using websockets
#ASGI_APPLICATION = "core.asgi.application" # new line added for websocket

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",  # Use Redis in production
#     },
# } # for websockets



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'employee_db',
        'USER': 'root',
        'PASSWORD': 'gautam_prog',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}





# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [],
#     'DEFAULT_PERMISSION_CLASSES': [],
#     'UNAUTHENTICATED_USER': None
# }

# I am using Redis DB 1 for Django caching but Redis DB 0 for celery task 
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Redis running on port 6379
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            
        }
    }
}


JWT_SETTINGS = {
    'SECRET_KEY': 'gautam',  # Change this to a secure secret key
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
}



# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # Example: Gmail SMTP server
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'gautam.agarwal@grayquest.com'
# EMAIL_HOST_PASSWORD = 'mdbo tlyb lzqw rxpd'  # Use environment variables for security
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER






EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))  # Convert to int
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"  # Convert to boolean
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

#'DIRS': [os.path.join(BASE_DIR, 'templates')],



# Redis as the message broker
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Backend for storing task results (optional)
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Task serialization format
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'



# if DEBUG:
#     INSTALLED_APPS += [
#         'debug_toolbar',
#     ]
    
#     MIDDLEWARE += [
#         'debug_toolbar.middleware.DebugToolbarMiddleware',
#     ]
    
#     INTERNAL_IPS = [
#         '127.0.0.1',
#     ]   # all this were debugger settings



LOGGING = {
    'version': 1,
    'disable_existing_loggers':False,  # Disable all other logs except the ones we specify
    'formatters': {
        'detailed': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',  # The curly brace style is used in the format
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Capture all log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'django.log'),
            'formatter': 'detailed',  # Use the 'detailed' formatter for timestamps and log levels
        },
    },
    'loggers': {
        'django': {  # This disables the default Django logger
            'handlers': ['file'],
            'level': 'CRITICAL',  # Only capture CRITICAL logs for Django (no unnecessary logs)
            'propagate': False,
        },
        'core': {  # Custom logger for your project
            'handlers': ['file'],
            'level': 'DEBUG',  # Capture DEBUG level logs for your app
            'propagate': False,  # Prevent it from propagating to the parent logger
        },
    },
}



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,  # Keep existing loggers
#     'formatters': {
#         'detailed': {
#             'format': '{asctime} {levelname} {name} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'detailed',
#         },
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'django.log',
#             'formatter': 'detailed',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }



