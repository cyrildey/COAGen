#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/caogen/CAOGen')
 
from app import app as application