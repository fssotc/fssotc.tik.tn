import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Check if debug toolbar is installed to add it to INSTALLED_APPS and
# MIDDLEWARES
try:
    import debug_toolbar
    DEBUG_TOOLBAR_INSTALLED = True
except ImportError:
    DEBUG_TOOLBAR_INSTALLED = False

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'after_response',
    'django_csv_exports',
    'wordpress',
    'db',
    'website',
    'blog',
    'inscription',
    'quiz',
    'event',
    'nested_admin',
    'bootstrap3',  # optional module for making bootstrap forms easier
]

if DEBUG_TOOLBAR_INSTALLED:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

if DEBUG_TOOLBAR_INSTALLED:
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'project.wsgi.application'

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

DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Tunis'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR + '/upload/'
MEDIA_URL = '/upload/'

CSP_DEFAULT_SRC = (
    "'self'",
)
CSP_IMG_SRC = (
    "'self'",
    "https://stats.g.doubleclick.net",
    "https://api.admin.tik.tn",
    "https://www.google-analytics.com",
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    # "stats.g.doubleclick.net",
    "https://api.admin.tik.tn",
    "https://www.google-analytics.com",
    "https://pagead2.googlesyndication.com",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "https://fonts.googleapis.com",
)
CSP_OBJECT_SRC = (
    "'none'",
)
CSP_CONNECT_SRC = (
    "'self'",
    "https://api.admin.tik.tn",
    "https://pagead2.googlesyndication.com",
)
CSP_FRAME_SRC = (
    "https://googleads.g.doubleclick.net",
)
CSP_REPORT_URI = 'https://api.admin.tik.tn/report/csp'
CSP_REPORT_ONLY = False

FILE_UPLOAD_MAX_MEMORY_SIZE = 50214400  # 50 M
DATA_UPLOAD_MAX_MEMORY_SIZE = 50214400  # 50 M


DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '/static/website/vendor/jquery-3.2.1.min.js'
}


from .settings_secret import *
