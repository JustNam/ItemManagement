import re
import functools

from flask import request

from utilities.message import error_message
from marshmallow import ValidationError


def validate_by_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def func_with_decorator(*args, **kwargs):

            try:
                data = convert_request_to_JSON(request)
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


def convert_request_to_JSON(request):
    if not request.is_json:
        raise ValidationError('Content-type must be "application/json"')

    try:
        data = request.json
    except:
        raise ValidationError('Wrong JSON format.')
        # return error_message('Wrong JSON format.', 400)
    return data


def validate_username(string):
    regex = re.compile('^[A-Za-z0-9]+$')
    if not regex.match(string):
        raise ValidationError('Username must contain only lowercase letters, numbers.')


def validate_category_name(string):
    regex = re.compile('^[A-Za-z0-9]+$')
    if not regex.match(string):
        raise ValidationError('Category name must contain only lowercase letters, numbers.')


def validate_item_title(string):
    regex = re.compile('^[a-zA-Z0-9\s]+$')
    if not regex.match(string):
        raise ValidationError('Item title must contain only lowercase letters, numbers, spaces.')

    if string[0] == ' ' or string[len(string) - 1] == ' ':
        raise ValidationError('Item title must not start or end with space.')

    regex = re.compile('(?!.*[\\s]{2})')
    if not regex.match(string):
        raise ValidationError('Item title must not contain 2 continuous spaces.')
