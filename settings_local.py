DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Arcady Chumachenko', 'arcady.chumachenko@gmail.com'),
    ('Ivan Kouznetsov', 'ikenovodvorsky@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'rttv.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

MEDIA_ROOT = './media/'
MEDIA_URL = '/i/'
ADMIN_MEDIA_PREFIX = '/i/admin/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'arcady.chumachenko@gmail.com'
EMAIL_HOST_PASSWORD = 'gPIl3EjI9kQCaT'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

THUMBNAIL_DEBUG = True
