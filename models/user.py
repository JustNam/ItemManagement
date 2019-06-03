from sqlalchemy_json import MutableJson
from marshmallow import ValidationError

from db import db
from models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    __public__ = ['id', 'username']
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(30), nullable=False, unique=True)
    password_hash = db.Column(db.VARCHAR(87), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    categories = db.relationship("Category", back_populates="user")
    items = db.relationship("Item", back_populates="user")

    handles = db.Column(MutableJson)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return "User ({})".format(self.username)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def check_existence_of_name(cls, username, id=-1):
        """ Check the existence of given name
        'id' will be passed if the method is used in updating function
        """
        user = User.find_by_username(username)
        if user:
            raise ValidationError({
                'title:': 'Username "{}" already exists.'.format(username)
            })
        return False
