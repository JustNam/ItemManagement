from marshmallow import Schema, fields, validate, post_load

from models.category import Category
from utilities.validate import validate_category_name


class CategorySchema(Schema):
    name = fields.Str(required=True,
                      validate=[validate.Length(min=1,
                                                max=30,
                                                error='Category name must contain 1 to 30 characters.'),
                                validate_category_name])
    user_id = fields.Int(required=True)

    @post_load
    def make_category(self, data):
        return Category(**data)

    class Meta:
        strict = True
