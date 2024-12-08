from .base import *

DEBUG = True
SECRET_KEY = "django-insecure-xp51pjd!)y3c51t)do+25^cu#fq@2qa#xh$bfidj0zxaj=ob$y"

REPORTED_BLOCKLIST_DAYS = 30
PAYPAL_MODE = 'sandbox'

SITE_URL = 'http://localhost:8000'
ALLOWED_HOSTS = []
INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    '127.0.0.1', 
]

CORS_ALLOWED_ORIGINS = []
CORS_TRUSTED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),  
        'USER': os.environ.get('DB_USER'),        
        'PASSWORD': os.environ.get('DB_PASSWORD'),       
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
