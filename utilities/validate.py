import functools

from flask import request

from utilities.message import error_message
from marshmallow import ValidationError


def validate_by_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def func_with_decorator(*args, **kwargs):

            try:
                data = convert_request_to_JSON()
            except ValidationError as e:
                return error_message(e.messages[0], 400)

            data['category_id'] = kwargs.get('category_id')
            data['item_id'] = kwargs.get('item_id')

            try:
                data = schema().load(data).data
            except ValidationError as e:
                return error_message('The submitted data does not meet the regulations',
                                     400,
                                     errors=e.messages)
            return func(data, *args, **kwargs)

        return func_with_decorator

    return decorator


def convert_request_to_JSON():
    if not request.is_json:
        raise ValidationError('Content-type must be "application/json"')

    try:
        data = request.json
    except:
        raise ValidationError('Wrong JSON format.')
    return data
