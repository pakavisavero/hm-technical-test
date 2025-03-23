from pathlib import Path
from django.db import connection
from dotenv import load_dotenv

import os
import django
import json

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-n3j0m9-=3jubjwa*bn6v$%*&h3e$gc2*5@j*+#ibpvkh$i@2rl'
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'https://hm-technical-test-production.up.railway.app',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'engine',
    'product']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "engine.middleware.ModuleCheckMiddleware",
]

ROOT_URLCONF = 'hashmicro_test.urls'

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
                'engine.context_processors.module_apps',
            ],
        },
    },
]

WSGI_APPLICATION = 'hashmicro_test.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
    }
}

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "engine/static"),
]

# Ensure this is correctly set for production
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Define the directory for error templates
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates/errors')]

# Set custom error handlers
HANDLER404 = 'django.views.defaults.page_not_found'
HANDLER403 = 'django.views.defaults.permission_denied'

# Load installed modules from a JSON file instead of querying the database
# MODULES_FILE = os.path.join(BASE_DIR, "installed_modules.json")

# if os.path.exists(MODULES_FILE):
#     with open(MODULES_FILE) as f:
#         installed_modules = json.load(f)
#         INSTALLED_APPS += installed_modules