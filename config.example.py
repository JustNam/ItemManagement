import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 900
    NUMBER_OF_RECORDS_IN_ONE_PAGE = 10
    SECRET_KEY = 'secretkey'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE', 'mysql://user:password@localhost/database')
    ENV = 'production'


class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE', 'mysql://user:281096^^@localhost/database')
    NUMBER_OF_RECORDS_IN_ONE_PAGE = 3
    ENV = 'development'
    DEBUG = True
