from pathlib import Path
import os
from decouple import config
from dotenv import load_dotenv
load_dotenv()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%mhsz76ph5v_8^xl8wj$zo=wz&#-cyv_*dirc%p_p9oe#%_!ui'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "queueau-beta.onrender.com"]


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'user',
    'request',
    'django_celery_results',
    'django_celery_beat',

]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'QueueAU.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'QueueAU.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

import dj_database_url


DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_DIRS = [os.path.join(BASE_DIR,'request/static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SMTP Settings


EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'apikey')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
"""


RECAPTCHA_SITE_KEY   = config("RECAPTCHA_SITE_KEY", default="sitekey")
RECAPTCHA_SECRET_KEY = config("RECAPTCHA_SECRET_KEY", default="secretkey")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Allow both DEBUG and INFO messages
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_events.log'),
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',  # Django internals still log INFO and above
            'propagate': True,
        },
        'custom_logger': {
            'handlers': ['file'],
            'level': 'DEBUG',  # Capture DEBUG logs for custom usage
            'propagate': False,
        },
    },
}

import ssl

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Handle SSL for Upstash (optional: upgrade to CERT_REQUIRED in production)
cert_reqs = os.getenv('CELERY_SSL_CERT_REQS', 'none').upper()

# Map string to ssl module constant
cert_options = {
    'CERT_NONE': ssl.CERT_NONE,
    'CERT_OPTIONAL': ssl.CERT_OPTIONAL,
    'CERT_REQUIRED': ssl.CERT_REQUIRED
}

cert_setting = cert_options.get(f'CERT_{cert_reqs.upper()}', ssl.CERT_NONE)

CELERY_BROKER_USE_SSL = {'ssl_cert_reqs': cert_setting}
CELERY_REDIS_BACKEND_USE_SSL = {'ssl_cert_reqs': cert_setting}


# Tell Celery to connect using SSL (required for Upstash)
CELERY_BROKER_USE_SSL = {
    'ssl_cert_reqs': ssl.CERT_NONE
}

CELERY_REDIS_BACKEND_USE_SSL = {
    'ssl_cert_reqs': ssl.CERT_NONE
}



TWILIO_ACCOUNT_SID = 'AC956827098b8a33dba0e2eea01e1a9eb1'
TWILIO_AUTH_TOKEN = 'd3512f94f4e34216128aa975447803ee'
TWILIO_VERIFY_SERVICE_SID = 'VA7035f58098dd270d44718b5b5f3918d3'


