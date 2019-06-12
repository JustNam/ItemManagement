from app import db
from models.base import BaseModel


class Category(BaseModel):
    __tablename__ = 'categories'
    __public__ = ['id', 'name', 'created_on', 'updated_on']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(30), nullable=False, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='categories')
    items = db.relationship('Item', back_populates='category',
                            cascade='all',
                            lazy='dynamic')

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)

    def __repr__(self):
        return 'Category ({}, {})'.format(self.name, self.user_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).one_or_none()

