from .base import *
import os
DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = [os.environ['DJANGO_ALLOWED_HOST_NAME']]

try:
    from .local import *
    LOCAL_EXISTS = True
except ImportError:
    print('Local settings were not found!')
    LOCAL_EXISTS = False

try:
    GITHUB_ACCESS_KEY = os.environ['CRASHKID_GITHUB_ACCESS_TOKEN']
except KeyError:
    if LOCAL_EXISTS:
        GITHUB_ACCESS_KEY = LOCAL_GITHUB_ACCES_KEY  # defined in the .local settings file
    else:
        GITHUB_ACCESS_KEY = 'n/A'
