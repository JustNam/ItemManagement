from marshmallow import ValidationError

from db import db
from models.base import BaseModel
from utilities.message import error_message


class Item(BaseModel):
    __tablename__ = 'items'
    __public__ = ["id", "title", "description", "created_on", "updated_on"]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(30), nullable=False)
    description = db.Column(db.String, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship("Category", back_populates="items")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="items")

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).one_or_none()


    @classmethod
    def check_existence_of_title(cls, title, id=-1):
        """ Check the existence of given title
        'id' will be passed if the method is used in updating function
        """
        item = Item.find_by_title(title)
        if item:
            if (id != -1) and (item.id == id):
                return False
            raise ValidationError({
                'title:': 'Item with title "{}" already exists.'.format(title)
            })
        return False
