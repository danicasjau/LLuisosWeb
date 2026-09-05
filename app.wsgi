import os
import sys

# Ensure the root project directory is in the Python module search path
if '__file__' in globals():
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
else:
    PROJECT_ROOT = os.path.abspath('.')
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import the Flask instance as 'application' (WSGI standard) and 'app'
from app import app as application
app = application

if __name__ == "__main__":
    application.run()
