# Django settings for rttv project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Arcady Chumachenko', 'arcady.chumachenko@gmail.com'),
    ('Ivan Kouznetsov', 'ikenovodvorsky@gmail.com'),
)

MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True



# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ch8^i(5nr6yl0!x7c&k+_*%=va$xdd+3e-==ga*24%8_r6vsd3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',

  	"django.middleware.locale.LocaleMiddleware",
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",

    "context_processors.common",
    "context_processors.widgets",
)

OUR_APPS = (
    'django.contrib.sites',
    'django.contrib.flatpages',

    'net',
    'places',
    'photo',
    'wall',
    'blog',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.comments',
    
    'django_registration',
    'dbsettings',

    'sorl.thumbnail',
) + OUR_APPS

ugettext = lambda s: s

LANGUAGE_CODE = 'Ru-ru';
LANGUAGES = (
    ('ru', ugettext('Russian')),
    ('en', ugettext('English')),
    ('ar', ugettext('Arabic')),
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/me/'
ACCOUNT_ACTIVATION_DAYS = 14

try:
    from settings_local import *
except ImportError:
    pass
