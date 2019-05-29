from app import ma
from marshmallow import validate, fields


class ItemSchema(ma.Schema):
    title = fields.Str(required=True,
                       validate=validate.Length(min=6,
                                                max=30,
                                                error='Username must contain 6 to 30 characters.'))
    description = fields.Str(required=False)

