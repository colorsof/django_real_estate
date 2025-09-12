"""Local Django settings (development)

This file is intended for local development and is loaded when
`DJANGO_SETTINGS_MODULE` is set to `config.settings.local`.

Purpose
- Load environment variables from `.envs/.env.local` when present.
- Provide development-friendly defaults (DEBUG=True).
- Read and normalise `DJANGO_ADMIN_URL` so the admin site can be
    exposed at a custom path (for example: `supersecret/`).

Important environment variables
- DJANGO_SECRET_KEY: overrides the default secret key.
- DJANGO_ADMIN_URL: the path segment where admin is exposed. Examples:
        - "supersecret/" -> admin available at /supersecret/
        - "supersecret"  -> also works (will be normalized)

Usage
- Keep DEBUG=True for local dev. Do NOT use this file in production.
"""

from os import getenv, path

from dotenv import load_dotenv

from .base import *  # noqa

from .base import BASE_DIR

local_env_file = path.join(BASE_DIR, '.envs', '.env.local')

if path.isfile(local_env_file):
    load_dotenv(local_env_file)
    
DEBUG = True

SITE_NAME = getenv('SITE_NAME')


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-!z0!tvz7*gbvo$x35b#9j!5r__yar+5=g(y*zh=%@u-y00-s6o'

SECRET_KEY = getenv(
    'DJANGO_SECRET_KEY',
    'rgJ4KsiINJjcmp-vBC8s2Kmvcw8Sh9oCRIuh6F-qUgyZGC3VbGE'
)

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0' ]

# Read ADMIN_URL from env and normalize it to 'name/' form (no leading slash)
_raw_admin = getenv('DJANGO_ADMIN_URL') or 'admin/'
_admin_stripped = _raw_admin.strip('/')
# e.g. 'supersecret/'
ADMIN_URL = f"{_admin_stripped}/"
# Ensure Django redirects to the configured admin login URL
LOGIN_URL = f"/{_admin_stripped}/login/"
EMAIL_BACKENG= 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = getenv('EMAIL_PORT')
DEFAULT_EMAIL_FROM = getenv('DEFAULT_FROM_EMAIL')
DOMAIN = getenv('DOMAIN')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(name)-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}