from marshmallow import Schema, fields


class CategorySchema(Schema):
    name = fields.Str(required=True)

