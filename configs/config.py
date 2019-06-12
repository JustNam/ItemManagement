class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 900
    ITEMS_PER_PAGE = 10
    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = 'w6kt4g32y3'
