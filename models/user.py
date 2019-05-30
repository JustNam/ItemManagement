from sqlalchemy_json import MutableJson

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
