import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/dkoder/SBHS-debakanta/local/lib/python2.7/site-packages/')

# Add the app's directory to the PYTHONPATHr
sys.path.append('/home/dkoder/sbhs/')
sys.path.append('/home/dkoder/sbhs/sbhs_server/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'sbhs_server.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/dkoder/SBHS-debakanta/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()