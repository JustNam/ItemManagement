import re

from marshmallow import validate, fields, post_load, ValidationError

from app import marshmallow
from models.user import User


def _validate_username(string):
    regex = re.compile('^[A-Za-z0-9]+$')
    if not regex.match(string):
        raise ValidationError('Username must contain only lowercase letters, numbers.')


class UserSchema(marshmallow.Schema):
    id = fields.Int()
    username = fields.Str(required=True,
                          validate=[validate.Length(min=6,
                                                    max=30,
                                                    error='Username must contain 6 to 30 characters.'),
                                    _validate_username])
    password = fields.Str(required=True,
                          validate=validate.Length(min=6,
                                                   error='Password must contain more than 6 characters.'))

    @post_load
    def make_user(self, data):
        return User(**data)

    class Meta:
        strict = True
