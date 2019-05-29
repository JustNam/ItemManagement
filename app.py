from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object('config')
jwt = JWTManager(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from controllers import *