import os
from pathlib import Path
from decouple import config

# --- BASE DIR & ENV ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', 'unsafe-default-key')

# --- APPLICATIONS ---
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portfolio',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- URL & WSGI ---
ROOT_URLCONF = 'portfolioproject.urls'
WSGI_APPLICATION = 'portfolioproject.wsgi.application'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', ''),
        'PASSWORD': config('DB_PASSWORD', ''),
        'HOST': config('DB_HOST', ''),
        'PORT': config('DB_PORT', ''),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        } if 'mysql' in config('DB_ENGINE', '') else {},
    }
}

# --- PASSWORD VALIDATORS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = config('LANGUAGE_CODE', 'en-us')
TIME_ZONE = config('TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA ---
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [BASE_DIR / 'portfolio' / 'static']  # Dev static files
STATIC_ROOT = BASE_DIR / 'staticfiles'                  # Collected static files
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise: gzip + caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- SECURITY / HOSTS ---
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    config('RAILWAY_APP_URL', 'portfolio-production-3e1e.up.railway.app')  # Your Railway app URL
]

# --- EMAIL ---
EMAIL_BACKEND = config('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', '')
EMAIL_PORT = int(config('EMAIL_PORT', 587))
EMAIL_USE_TLS = config('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = config('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# --- DEFAULTS ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'portfolio:admin-login'

# --- PRODUCTION TIPS ---
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
