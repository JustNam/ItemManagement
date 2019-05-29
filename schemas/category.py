from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    name = fields.Str(required=True,
                      validate=validate.Length(min=6,
                                               max=30,
                                               error='Category name must contain 6 to 30 characters.'))
