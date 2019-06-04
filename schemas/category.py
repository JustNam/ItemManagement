import re

from marshmallow import Schema, fields, validate, post_load, ValidationError

from models.category import Category


def _validate_category_name(string):
    regex = re.compile('^[A-Za-z0-9\\s]+$')
    if not regex.match(string):
        raise ValidationError('Category name must contain only lowercase letters, numbers, spaces.')

    if string[0] == ' ' or string[len(string) - 1] == ' ':
        raise ValidationError('Category name must not start or end with space.')

    regex = re.compile('(?!.*[\\s]{2})')
    if not regex.match(string):
        raise ValidationError('Category name must not contain 2 continuous spaces.')


class CategorySchema(Schema):
    name = fields.Str(required=True,
                      validate=[validate.Length(min=1,
                                                max=30,
                                                error='Category name must contain 1 to 30 characters.'),
                                _validate_category_name])

    @post_load
    def make_category(self, data):
        return Category(**data)

    class Meta:
        strict = True
