import os

from configs.config import Config


class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE', 'mysql://user:password@localhost/database')
    ITEMS_PER_PAGE = 3
    ENV = 'development'
    DEBUG = True
