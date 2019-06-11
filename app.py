import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

ENV = os.environ.get('ENV', 'development')
if ENV == 'development':
    app.config.from_object('config.DevelopmentConfig')
elif ENV == 'production':
    app.config.from_object('config.ProductionConfig')
jwt = JWTManager(app)
db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

from controllers import *
