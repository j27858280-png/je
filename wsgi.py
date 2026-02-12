# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below assumes you're using Flask. If you are using a different web
# framework, you'll need to change the code accordingly.

import sys
import os

# Add the current directory to the path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables for production with SQLite
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('DATABASE_URL', f'sqlite:///{path}/instance/worker_management.db')
os.environ.setdefault('SECRET_KEY', 'your-super-secret-key-change-in-production')

# Import the Flask application
from run import app as application

# For debugging, you can uncomment the following lines:
# import logging
# logging.basicConfig(level=logging.DEBUG)
# application.logger.setLevel(logging.DEBUG)