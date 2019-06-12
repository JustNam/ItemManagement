import os

from configs.config import Config


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE', 'mysql://user:password@localhost/database')
    ENV = 'production'
