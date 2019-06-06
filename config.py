import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 900
    NUMBER_OF_RECORDS_IN_ONE_PAGE = 10
    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = 'w6kt4g32y3'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE', 'mysql://root:281096^^@localhost/item_management')
    ENV = 'production'


class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE', 'mysql://root:281096^^@localhost/item_management')
    NUMBER_OF_RECORDS_IN_ONE_PAGE = 3
    ENV = 'development'
    DEBUG = True
