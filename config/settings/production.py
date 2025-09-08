from os import getenv, path

from dotenv import load_dotenv

from .base import *  # noqa

from .base import BASE_DIR

local_env_path = path.join(BASE_DIR, '.envs', '.env.local')

if path.isfile(local_env_file):
    load_dotenv(local_env_file)
    

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-!z0!tvz7*gbvo$x35b#9j!5r__yar+5=g(y*zh=%@u-y00-s6o'

SECRET_KEY = getenv(
    'DJANGO_SECRET_KEY',
    
)

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = []

ADIMNS=[('Bernard Gitau', 'bernadx90@gmail.com')
    ]