import re

from marshmallow import validate, fields, post_load, ValidationError

from app import marshmallow
from models.item import Item
from schemas.category import CategorySchema
from schemas.user import UserSchema


def _validate_item_title(string):
    regex = re.compile('^[a-zA-Z0-9\\s]+$')
    if not regex.match(string):
        raise ValidationError('Item title must contain only lowercase letters, numbers, spaces.')

    if string[0] == ' ' or string[len(string) - 1] == ' ':
        raise ValidationError('Item title must not start or end with space.')

    regex = re.compile('(?!.*[\\s]{2})')
    if not regex.match(string):
        raise ValidationError('Item title must not contain 2 continuous spaces.')


class ItemSchema(marshmallow.Schema):
    id = fields.Int()
    title = fields.Str(required=True,
                       validate=[validate.Length(min=1,
                                                 max=30,
                                                 error='Item title must contain 1 to 30 characters.'),
                                 _validate_item_title])
    description = fields.Str(required=False)
    user = fields.Nested(UserSchema, exclude=('password', ))
    category = fields.Nested(CategorySchema, exclude=('user', ))
    updated_on = fields.DateTime('%m/%d/%Y, %H:%M:%S')
    created_on = fields.DateTime('%m/%d/%Y, %H:%M:%S')

    @post_load
    def make_item(self, data):
        return Item(**data)

    class Meta:
        strict = True
