from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

env = environ.Env(
    DJANGO_SECRET_KEY=(str, 'unsafe-secret-key'),
    DJANGO_DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, ['127.0.0.1', 'localhost']),
    DJANGO_CSRF_TRUSTED_ORIGINS=(list, ['http://127.0.0.1', 'http://localhost']),
    CORS_ALLOWED_ORIGINS=(list, ['http://localhost:3000']),
    DJANGO_DATABASE_URL=(str, f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
    REDIS_URL=(str, 'redis://redis:6379/0'),
    CACHE_TTL=(int, 60),
    DJANGO_TIME_ZONE=(str, 'Europe/Moscow'),
    API_PAGE_SIZE=(int, 10),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
    DJANGO_TEST_USER_USERNAME=(str, 'meowhub_demo'),
    DJANGO_TEST_USER_EMAIL=(str, 'demo@meowhub.local'),
    DJANGO_TEST_USER_PASSWORD=(str, 'meowhub123'),
    DEMO_DATA_ENABLED=(bool, True),
)
env_file = PROJECT_ROOT / '.env'
if env_file.exists():
    env.read_env(env_file)

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env.list('DJANGO_CSRF_TRUSTED_ORIGINS')
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'cats',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meowhub_backend.urls'

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

WSGI_APPLICATION = 'meowhub_backend.wsgi.application'
ASGI_APPLICATION = 'meowhub_backend.asgi.application'

DATABASES = {'default': env.db('DJANGO_DATABASE_URL')}

REDIS_URL = env('REDIS_URL')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}
CACHE_TTL = env.int('CACHE_TTL')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = env('DJANGO_TIME_ZONE')
USE_I18N = True
USE_L10N = False
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': env.int('API_PAGE_SIZE'),
}

DJOSER = {
    'LOGIN_FIELD': 'username',
    'SERIALIZERS': {},
}

SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')
if not DEBUG:
    if 'SESSION_COOKIE_SECURE' not in env.ENVIRON:
        SESSION_COOKIE_SECURE = True
    if 'CSRF_COOKIE_SECURE' not in env.ENVIRON:
        CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TEST_USER_USERNAME = env('DJANGO_TEST_USER_USERNAME')
TEST_USER_EMAIL = env('DJANGO_TEST_USER_EMAIL')
TEST_USER_PASSWORD = env('DJANGO_TEST_USER_PASSWORD')
DEMO_DATA_ENABLED = env.bool('DEMO_DATA_ENABLED')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name}: {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO'},
        'cats': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}
