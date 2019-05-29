import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE', 'sqlite:///data.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'hodns'