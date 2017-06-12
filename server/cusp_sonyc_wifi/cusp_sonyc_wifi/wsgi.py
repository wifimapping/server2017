"""
WSGI config for research project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

'''
# Uncomment this and comment out the rest of the file when getting:
#    "RuntimeError: populate() isn't reentrant"
import os
def application(environ, start_response):
    if environ['mod_wsgi.process_group'] != '': 
        import signal
        os.kill(os.getpid(), signal.SIGINT)
    return ["killed"]
'''

# import
import os
import sys
import site

# declare variables
virtualenv_parent_dir = ""
path_to_django_project_parent = ""
virtualenv_python2 = ""
temp_path = ""

# configure
virtualenv_parent_dir = "/home/wifind"
virtualenv_python2 = "wifind_app"
path_to_django_project_parent = "/home/wifind/wifimapping/server"
django_project = "cusp_sonyc_wifi"

# Add the app's directory to the PYTHONPATH
temp_path = path_to_django_project_parent + "/" + django_project
sys.path.append( temp_path )

# Set DJANGO_SETTINGS_MODULE
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", django_project + ".settings" )

# Add the site-packages of the desired virtualenv
temp_path = virtualenv_parent_dir + "/" + virtualenv_python2 + "/local/lib/python2.7/site-packages"
site.addsitedir( temp_path )

# Activate your virtualenv
temp_path = virtualenv_parent_dir + "/" + virtualenv_python2 + "/bin/activate_this.py"
activate_this = os.path.expanduser( temp_path )

# in Python 2, just use execfile()
execfile( activate_this, dict( __file__ = activate_this ) )

# import django stuff - it is installed in your virtualenv, so you must import
#     after activating virtualenv.
from django.core.wsgi import get_wsgi_application

# load django application
application = get_wsgi_application()
