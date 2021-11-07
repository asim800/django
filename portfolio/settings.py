"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import io
import os
import environ

import pymysql
pymysql.install_as_MySQLdb()

from google.cloud import secretmanager

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-deqeyxz_%mub3skb&(j#7_t6)qhbthe@413a**dv980vf6@w1c'

# [START gaestd_py_django_secret_config]
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    # Use a local secret file, if provided

    env.read_env(env_file)
# [START_EXCLUDE]
elif os.getenv("TRAMPOLINE_CI", None):
    # Create local settings if running with CI, for unit testing

    placeholder = (
        f"SECRET_KEY=a\n"
        f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
    env.read_env(io.StringIO(placeholder))
# [END_EXCLUDE]
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
# [END gaestd_py_django_secret_config]

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
		'rest_framework',
		'ckeditor',
		'members',
		'mysite',
		'blogs',
		'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if os.getenv('GAE_APPLICATION', None):
	# Use django-environ to parse the connection string
	# DATABASES = {"default": env.db()}
	DATABASES = {
		# 'blogs': {
		# 		# 'ENGINE': 'django.db.backends.postgresql',
		# 		# 'HOST': '/cloudsql/asim800:us-central1:django-app1',  # '35.225.156.96', #
		# 		# 'USER': 'pblogsu',
		# 		# 'PASSWORD': 'pblogsu',
		# 		'ENGINE': 'django.db.backends.mysql',
		# 		'HOST':  '/cloudsql/asim800:us-central1:django-mysql-1',  # '35.225.156.96', #
		# 		'NAME': 'blogs',
		# 		'USER': 'pblog',
		# 		'PASSWORD': 'pblog',
		# },
		'default': {
				'ENGINE': 'django.db.backends.mysql',
				'HOST':  '/cloudsql/asim800:us-central1:django-mysql-1',  # '35.225.156.96', #
				'NAME': 'default1',  #BASE_DIR / 'db.Project',
				'USER': 'pblog',
				'PASSWORD': 'pblog',
		},
		'blog_db': {
				'ENGINE': 'django.db.backends.mysql',
				'HOST':  '/cloudsql/asim800:us-central1:django-mysql-1',  # '35.225.156.96', #
				'NAME': 'blogs',
				'USER': 'pblog',
				'PASSWORD': 'pblog',
		},
		'fin_db': {
				'ENGINE': 'django.db.backends.mysql',
				'HOST':  '/cloudsql/asim800:us-central1:django-mysql-1',  # '35.225.156.96', #
				'NAME': 'ohlcv',
				'USER': 'pblog',
				'PASSWORD': 'pblog',
		}
	}

	bucket_name = 'staging.asim800.appspot.com'
	DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
	GS_BUCKET_NAME = bucket_name
	GS_DEFAULT_ACL = 'publicRead' 
	# MEDIA_URL = 'https://storage.googleapis.com/'+bucket_name+'/'
	# MEDIA_URL = 'https://storage.googleapis.com/staging.asim800.appspot.com/'

	# DATABASES = {"default": env.db()}
elif os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
	DATABASES = {
		'default': {
				'ENGINE': 'django.db.backends.mysql',
				'HOST': '127.0.0.1',					
				'PORT': '5432', #'5432',
				'NAME': 'default1',  #BASE_DIR / 'db.Project',
				'USER': 'pblog',
				'PASSWORD': 'pblog',
		},
		'blog_db'  : {
				# 'ENGINE': 'django.db.backends.postgresql',
				'ENGINE': 'django.db.backends.mysql',
				'HOST': '127.0.0.1',					
				'PORT': '5432', #'5432',
				'NAME': 'blogs',  #BASE_DIR / 'db.Project',
				'USER': 'pblog',
				'PASSWORD': 'pblog',
		},
		'fin_db'  : {
				# 'ENGINE': 'django.db.backends.postgresql',
				'ENGINE': 'django.db.backends.mysql',
				'HOST': '127.0.0.1',					
				'PORT': '5432', #'5432',
				'NAME': 'ohlcv',  #BASE_DIR / 'db.Project',
				'USER': 'pblog',
				'PASSWORD': 'pblog',
		}
	}
else:
	DATABASES = {
			'default': {
					'ENGINE': 'django.db.backends.sqlite3',
					'NAME': BASE_DIR / 'db.sqlite3',
			},
			'blog_db': {
					'ENGINE': 'django.db.backends.sqlite3',
					'NAME': BASE_DIR / 'blog.db.sqlite3',
					# 'NAME': 'blogs',  #BASE_DIR / 'db.Project',
					# 'USER': 'pblog',
					# 'PASSWORD': 'pblog',
			}
	}


	# PROJECT_PATH = os.path.join(os.path.abspath(os.path.split(__file__)[0]), '..')
	# MEDIA_ROOT = os.path.join(PROJECT_PATH, 'site_media')
	# MEDIA_URL = '/site_media/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago' #'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'staticfiles'), ]

# DATABASE_ROUTERS = ['routers.db_routers.AuthRouter', 'router.db_routers.BlogRouter',]
DATABASE_ROUTERS = ['routers.db_routers.BlogRouter',]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# setup login redirection - redirects after after login
LOGIN_REDIRECT_URL 	= 'mysite-index'
LOGOUT_REDIRECT_URL = 'mysite-index'
