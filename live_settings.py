# Django settings for zombiewalrus project.
from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'zombiewalrus',                      # Or path to database file if using sqlite3.
        'USER': 'zombiewalrus',                      # Not used with sqlite3.
        'PASSWORD': 'walrus3775',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://media.zombiewalrusdetective.com/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = 'http://media.zombiewalrusdetective.com/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vc^lhhcsa6lcr2vd0=c--3vs)tn%l%^+vbese5(+ynair6p$=u'
