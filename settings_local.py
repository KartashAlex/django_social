DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Ike', 'ikenovodvorsky@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'rttv_social'             # Or path to database file if using sqlite3.
DATABASE_USER = 'ike'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TEMPLATE_DIRS = (
    '/Users/ivankuznetsov/dev/rttv_social/net/templates',
 	'/Users/ivankuznetsov/dev/rttv_social/photo/templates',
 	'/Users/ivankuznetsov/dev/rttv_social/places/templates',
 	'/Users/ivankuznetsov/dev/rttv_social/wall/templates',
)

EMAIL_HOST_USER = 'ikenovodvorsky@gmail.com'
EMAIL_HOST_PASSWORD = 'beta19ira'

MEDIA_ROOT = '/Users/ivankuznetsov/dev/rttv_social/media/'


MEDIA_URL = '/i/'