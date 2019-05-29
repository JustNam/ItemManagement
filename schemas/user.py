from app import ma
from marshmallow import validate, fields, post_load

from models.user import User
from utilities import generate_hash


class UserSchema(ma.Schema):
    username = fields.Str(required=True,
                          validate=validate.Length(min=6,
                                                   max=30,
                                                   error='Username must contain 6 to 30 characters.'))
    password = fields.Str(required=False,
                          validate=validate.Length(min=6,
                                                   error='Password must contain more than 6 characters.'))

    @post_load
    def make_user(self, data):
        data['password_hash'] = generate_hash(data.pop('password'))
        return User(**data)
