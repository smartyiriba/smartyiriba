import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv('DJANGO_DEBUG', 'false').lower() == 'true'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured('DJANGO_SECRET_KEY is required outside local development.')
    SECRET_KEY = 'local-development-only-do-not-deploy'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'rest_framework', 'apps.accounts', 'apps.catalog', 'apps.quotes', 'apps.core', 'apps.commerce']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.locale.LocaleMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages', 'apps.core.context_processors.business_contact']}}]
WSGI_APPLICATION = 'config.wsgi.application'
if os.getenv('POSTGRES_DB'):
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': os.environ['POSTGRES_DB'], 'USER': os.getenv('POSTGRES_USER', 'biz'), 'PASSWORD': os.environ['POSTGRES_PASSWORD'], 'HOST': os.getenv('POSTGRES_HOST', 'db'), 'PORT': os.getenv('POSTGRES_PORT', '5432')}}
elif DEBUG:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
else:
    raise ImproperlyConfigured('PostgreSQL configuration is required outside development.')
AUTH_USER_MODEL = 'accounts.User'
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.' + name} for name in ['UserAttributeSimilarityValidator', 'MinimumLengthValidator', 'CommonPasswordValidator', 'NumericPasswordValidator']]
LANGUAGE_CODE = 'fr'
LANGUAGES = [('fr', 'Français'), ('en', 'English')]
TIME_ZONE = 'Africa/Bamako'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAdminUser'], 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 'PAGE_SIZE': 20}
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Les coordonnées sont conservées dans chaque facture lors de son émission.
BUSINESS_ISSUER = {
    'name': os.getenv('BUSINESS_LEGAL_NAME', ''),
    'address': os.getenv('BUSINESS_ADDRESS', ''),
    'registration': os.getenv('BUSINESS_REGISTRATION', ''),
    'email': os.getenv('BUSINESS_EMAIL', ''),
}

BUSINESS_CONTACT = {
    'email': os.getenv('BUSINESS_CONTACT_EMAIL', 'contact@smartyiriba.org'),
    'secondary_email': os.getenv('BUSINESS_CONTACT_SECONDARY_EMAIL', 'smartyiriba@gmail.com'),
    'phone': os.getenv('BUSINESS_CONTACT_PHONE', ''),
    'whatsapp': os.getenv('BUSINESS_WHATSAPP', ''),
    'address': os.getenv('BUSINESS_CONTACT_ADDRESS', 'Sotuba, Bamako, Mali'),
    'hours': os.getenv('BUSINESS_CONTACT_HOURS', '09 h à 18 h · jours à confirmer'),
}
