from marshmallow import ValidationError

from app import db
from models.base import BaseModel


class Item(BaseModel):
    __tablename__ = 'items'
    __public__ = ['id', 'title', 'description', 'created_on', 'updated_on']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(30), nullable=False)
    description = db.Column(db.Text, nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='items')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='items')

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).one_or_none()

