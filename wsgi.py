import sys

from app import app as application

sys.path.insert(0, '/var/www/catalog')

application.secret_key = '3452@#$%@#$543254325jkljrtkelwrtjerw4^$ra--'

application.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://catalog:password@localhost/catalog')
