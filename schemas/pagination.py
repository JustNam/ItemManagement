from marshmallow import fields

from app import marshmallow
from schemas.item import ItemSchema


class PaginationSchema(marshmallow.Schema):
    last_page = fields.Int(required=True)
    current_page = fields.Int(required=True)
    items = fields.Nested(ItemSchema, required=True)
