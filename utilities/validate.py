import functools

from flask import request

from marshmallow import ValidationError
from errors import WrongJsonFormat, WrongContentTypeError, InvalidRequestDataError


def validate_by_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def func_with_decorator(*args, **kwargs):
            if not request.is_json:
                raise WrongContentTypeError()

            try:
                data = request.json
            except:
                raise WrongJsonFormat()

            try:
                data = schema().load(data).data
            except ValidationError as e:
                raise InvalidRequestDataError(e.message)
            return func(data, *args, **kwargs)

        return func_with_decorator

    return decorator
