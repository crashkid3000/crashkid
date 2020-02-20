from .base import *
import os
DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = [os.environ['DJANGO_ALLOWED_HOST_NAME']]

try:
    from .local import *
except ImportError:
    print('Local settings were not found.')

