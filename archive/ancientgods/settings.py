import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JINJA2_DIR = os.path.join(BASE_DIR, 'templates')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


DEBUG=True
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', 'localhost']

SECRET_KEY='b0mqvak1p2sqm6p#+8o8fyxf+ox(le)8&jh_5^sxa!=7!+wxj0'
ROOT_URLCONF='ancientgods.urls'

MIDDLEWARE_CLASSES=(
        'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'django_extensions',
        'debug_toolbar',
        'game',
    )

STATIC_URL='/static/'
STATIC_ROOT='static'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [ JINJA2_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'ancientgods.local_jinja2.environment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]
