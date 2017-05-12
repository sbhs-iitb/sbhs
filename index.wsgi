import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/vlabs/sbhs_vlabs/sbhs/local/lib/python2.7/site-packages/')

# Add the app's directory to the PYTHONPATHr
sys.path.append('/home/vlabs/sbhs_vlabs/sbhs/sbhs_server/')
sys.path.append('/home/vlabs/sbhs_vlabs/sbhs/sbhs_server/sbhs_server/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'sbhs_server.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/vlabs/sbhs_vlabs/sbhs/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()