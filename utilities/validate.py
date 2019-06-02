from marshmallow import ValidationError
import re


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

    if string[0] == ' ' or string[len(string)-1] == ' ':
        raise ValidationError('Item title must not start or end with space.')

    regex = re.compile('(?!.*[\\s]{2})')
    if not regex.match(string):
        raise ValidationError('Item title must not contain 2 continuous spaces.')
