from app import ma
from marshmallow import validate, fields
from utilities.validate import validate_item_title


class ItemSchema(ma.Schema):
    title = fields.Str(required=True,
                       validate=[validate.Length(min=1,
                                                 max=30,
                                                 error='Item title must contain 1 to 30 characters.'),
                                 validate_item_title])
    description = fields.Str(required=False)

    class Meta:
        strict = True
