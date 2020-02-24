from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ww2g6gdl%ii!a%4jz0a5dt_6#$4d$!0_0gp4&k$z^lzcj&00y5'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
    LOCAL_EXISTS = True
except ImportError:
    print('Local settings were not found...')
    LOCAL_EXISTS = False

try:
    GITHUB_ACCESS_KEY = os.environ['CRASHKID_GITHUB_ACCESS_TOKEN']
except KeyError:
    if LOCAL_EXISTS:
        GITHUB_ACCESS_KEY = LOCAL_GITHUB_ACCES_KEY  # defined in the .local settings file
    else:
        GITHUB_ACCESS_KEY = 'n/A'
