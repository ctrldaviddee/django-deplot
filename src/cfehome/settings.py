"""
Django settings for cfehome project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""


from email.policy import default
from decouple import config
from django.core.management.utils import get_random_secret_key
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR.parent
TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

PROJECT_NAME = config("PROJECT_NAME", default="Unset Project Name")


# default backend

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = config("EMAIL_HOST", cast=str, default=None)

EMAIL_PORT = config("EMAIL_PORT", cast=str, default='587') # Recommended

EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)

EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)  # Use EMAIL_PORT 587 for TLS

EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)  # EUse MAIL_PORT 465 for SSL

ADMIN_USER_NAME=config("ADMIN_USER_NAME", default="Admin user")
ADMIN_USER_EMAIL=config("ADMIN_USER_EMAIL", default=None)

MANAGERS=[]
ADMINS=[]

DEFAULT_FROM_EMAIL= EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS +=[
        (f'{ADMIN_USER_NAME}', f'{ADMIN_USER_EMAIL}')
    ]
    MANAGERS=ADMINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', cast=str, default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = [
    '.django-deploy.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.django-deploy.com',
]


# HTTPS
CSRF_COOKIE_SECURE= not DEBUG
SECCION_COOKIE_SECURE = not DEBUG

if DEBUG:
    ALLOWED_HOSTS = ['*']
    
RAILWAY_HOSTS = [
    "healthcheck.railway.app",
    ".railway.internal",
    ".up.railway.app",
    "django-deplot.railway.internal",
]

for host in RAILWAY_HOSTS:
    ALLOWED_HOSTS.append(host)
    for protocol in ["http", "https"]:
        if host.startswith("."):
            CSRF_TRUSTED_ORIGINS.append(f"{protocol}://*{host}")
        else:
            CSRF_TRUSTED_ORIGINS.append(f"{protocol}://{host}")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'commando',
]

if DEBUG:
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cfehome.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, ],
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

WSGI_APPLICATION = 'cfehome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if DATABASE_URL := config("DATABASE_URL", cast=str, default=''):
    import dj_database_url
    if DATABASE_URL.startswith('postgres://') or DATABASE_URL.startswith('postgresql://'):
        DATABASES = {
            "default" : dj_database_url.config(
                default=DATABASE_URL,    
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'


# Send static files here. 
# Locked files that do not change during runtime
# External static file server
STATIC_ROOT = BASE_DIR / 'static_root'
STATIC_ROOT.mkdir(parents=True, exist_ok=True)


# Retain a copy of static files here. e.g: custom css
# Unlocked files that change during dev
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]
for dir in STATICFILES_DIRS:
    dir.mkdir(parents=True, exist_ok=True)
    
    
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_URL = config("REDIS_URL", default="")

# REDIS CACHE
if REDIS_URL:
    print(REDIS_URL)
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
}