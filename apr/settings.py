"""
Django settings for apr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(i=16yxj@9buj^9y_j0w)qhdm5ppk+8)g5k*0v^5*-r=@i5o+k'

# Application definition

INSTALLED_APPS = (
    'suit',
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    # third party
    'compressor',
    'schedule',
    'crispy_forms',
    'django_select2',
    'allauth',
    'allauth.account',
    'debug_toolbar',
    'datatableview',
    'randomslugfield',
    'cacheops',
    'suit_redactor',
    'django_js_reverse',
    # custom
    'appointments',
    'users',
    'doctors',
    'assistants',
    'venues',
    'customers',
    'opening_hours',
    'subscriptions',
    'reminders',
    'invoices',
    'notes',
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'apr.urls'

WSGI_APPLICATION = 'apr.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                # default
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

                # custom
                "customers.context_processors.current_customer_processor",
                'core.context_processors.site_processor',
                'core.context_processors.debug_processor',
                "doctors.context_processors.doctor_processor",
                "venues.context_processors.venue_processor",
                "assistants.context_processors.assistant_processor",
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'django.template.loaders.eggs.Loader',
                ]),
            ],
            # 'loaders': [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            #     'django.template.loaders.eggs.Loader',
            # ],
            'debug': False,
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# COMPRESSOR
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']

STATIC_URL = '/static/'

# crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_USERNAME_BLACKLIST = ['mosh', 'moshthepitt', 'kelvin', 'nicole', 'jay']
LOGIN_REDIRECT_URL = '/new'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379/8'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/8'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_ENABLE_UTC = True

# APR STUFF
REMINDER_FROM_EMAIL = "noreply-reminder <no-reply@appointware.com>"
REMINDER_FROM_EMAIL_ONLY = "no-reply@appointware.com"

# CACHE OPS
CACHEOPS_REDIS = {
    'host': 'localhost',  # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 7,             # SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended
    'socket_timeout': 3,
}
CACHEOPS_DEGRADE_ON_FAILURE = True
CACHEOPS = {
    # automatically cache everything
    '*.*': ('all', 60 * 10),
}

try:
   from local_settings import *
except ImportError, e:
   pass
