"""
Django settings for videoflix project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m78s&^ux7*=o0gkro^atoun8c7r8sbo22dthk60fh!w$lf@s39'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost']
CORS_ALLOWED_ORIGINS = ['http://localhost:4200','http://localhost:5500','http://127.0.0.1:5500','https://julia-wessolleck.developerakademie.net']

AUTH_USER_MODEL = 'videoflixApp.User'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media') #BASE_DIR ist videoflix
MEDIA_URL = '/media/'  # localhost/media    greift auf den Medienordner zu
# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'videoflixApp', 
    'videoflixApp.apps.VideoflixappConfig', # important for signals
    'rest_framework',
    'rest_framework.authtoken', #important for usage of Token
    'rest_auth',  #pip install django-rest-auth
    'rest_auth.registration',   
    'django_rest_passwordreset',  #pip install django-rest-passwordreset
    'corsheaders',   #pip install django-cors-headers  important CORS
    'debug_toolbar',
    'rest_framework_simplejwt',
    'drf_yasg'
    
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  #important CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
]


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    
    # ...
]


ROOT_URLCONF = 'videoflix.urls'

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

WSGI_APPLICATION = 'videoflix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'todolist.views.EmailOrUsernameAuthentication',# Stellen Sie sicher, dass Sie den Pfad zu Ihrer Authentifizierungsklasse angeben
        'rest_framework.authentication.TokenAuthentication'
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ]
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT =  587 #465
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mucki6412@gmail.com'
EMAIL_HOST_PASSWORD = 'atoh ynmm zlzo iekr'

CACHES = {    
          "default": {       
              "BACKEND": "django_redis.cache.RedisCache",       
              "LOCATION": "redis://127.0.0.1:6379/1",        
              "OPTIONS": {            
                  "CLIENT_CLASS": "django_redis.client.DefaultClient"        
                  },        
              "KEY_PREFIX": "videoflix"    }
          }
