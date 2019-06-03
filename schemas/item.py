from marshmallow import validate, fields, post_load

from app import ma
from utilities.validate import validate_item_title
from models.item import Item


class ItemSchema(ma.Schema):
    title = fields.Str(required=True,
                       validate=[validate.Length(min=1,
                                                 max=30,
                                                 error='Item title must contain 1 to 30 characters.'),
                                 validate_item_title])
    description = fields.Str(required=False)

    @post_load
    def make_item(self, data):
        return Item(**data)

    class Meta:
        strict = True
