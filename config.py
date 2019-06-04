import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE', 'mysql://root:281096^^@localhost/item_management')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'hodns'
PER_PAGE = 3