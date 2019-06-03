from marshmallow import ValidationError

from db import db
from models.base import BaseModel
from utilities.message import error_message


class Category(BaseModel):
    __tablename__ = 'categories'
    __public__ = ["id", "name", "created_on", "updated_on"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="categories")
    items = db.relationship("Item", back_populates="category",
                            cascade="all, delete-orphan",
                            lazy='dynamic',
                            passive_deletes=True)

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)

    def __repr__(self):
        return "Category ({}, {})".format(self.name, self.user_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def check_existence(cls, id):
        category = Category.find_by_id(id)
        if not category:
            raise ValidationError('Can not find any category with id = "{}"'.format(id))
        return category

    def check_existence_of_item(self, item_id):

        item = self.items.filter_by(id=item_id).first()
        if not item:
            raise ValidationError("Can not find the item with id = {} in the category".format(item_id))
        return item

    @classmethod
    def check_existence_of_name(cls, name, id=-1):
        """ Check the existence of given name
        'id' will be passed if the method is used in updating function
        """
        category = Category.find_by_name(name)
        if category:
            if (id != -1) and (category.id == id):
                return False
            raise ValidationError({
                'title:': 'Category with name "{}" already exists.'.format(category.name)
            })
        return False
