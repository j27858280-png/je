# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below assumes you're using Flask. If you are using a different web
# framework, you'll need to change the code accordingly.

import sys
import os

# assuming the app is in a subdirectory called 'app'
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['FLASK_ENV'] = 'production'

from run import app as application

# For debugging, you can uncomment the following lines:
# import logging
# logging.basicConfig(level=logging.DEBUG)
# application.logger.setLevel(logging.DEBUG)