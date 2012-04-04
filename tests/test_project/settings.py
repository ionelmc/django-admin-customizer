# -*- coding: utf-8 -*-
import os
DEBUG = True

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'database.sqlite')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + DATABASE_ENGINE,
        'NAME': DATABASE_NAME
    },
}
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'admin_customizer',
    'test_app',
)
SITE_ID = 1
ROOT_URLCONF = 'test_project.urls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

SECRET_KEY = ADMIN_MEDIA_PREFIX = "DON'T MATTER"
