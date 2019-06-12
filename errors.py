from flask import jsonify
from app import app


class BaseError(Exception):

    def __init__(self, message, status_code, errors=None):
        Exception.__init__(self)
        self.message = message
        self.errors = errors
        self.status_code = status_code

    def to_dict(self):
        dictionary = dict(
            errors=self.errors,
            msg=self.message
        )
        return dictionary


class RecordNotFoundError(BaseError):
    def __init__(self, model_name, record_id):
        super(RecordNotFoundError, self).__init__(
            'Can not find any {} with id = {}.'.format(model_name, record_id),
            404
        )


class ItemNotFoundError(BaseError):
    def __init__(self, item_id):
        super(ItemNotFoundError, self).__init__(
            'Can not find any item with id = {} in the category.'.format(item_id),
            404
        )


class PageNotFoundError(BaseError):
    def __init__(self):
        super(PageNotFoundError, self).__init__(
            'Can not find the requested page.',
            404
        )


class DuplicateValueError(BaseError):
    def __init__(self, model_name, field, value):
        super(DuplicateValueError, self).__init__(
            'The submitted data does not meet the regulations',
            400,
            {
                field: '{} with {} = "{}" already exists.'.format(model_name, field, value)
            }
        )


class WrongPageNumberTypeError(BaseError):
    def __init__(self):
        super(WrongPageNumberTypeError, self).__init__(
            'The submitted parameter does not meet the regulations',
            400,
            {
                'page': [
                    'Not a valid integer.'
                ]
            }
        )


class ForbiddenError(BaseError):
    def __init__(self):
        super(ForbiddenError, self).__init__(
            'You are not allowed to perform this action.',
            403
        )


class InvalidCredentialsError(BaseError):
    def __init__(self):
        super(InvalidCredentialsError, self).__init__(
            'Invalid username or password',
            400
        )


class WrongContentTypeError(BaseError):
    def __init__(self):
        super(WrongContentTypeError, self).__init__(
            'Content-type must be "application/json"',
            400
        )


class WrongJsonFormatError(BaseError):
    def __init__(self):
        super(WrongJsonFormatError, self).__init__(
            'Wrong JSON format.',
            400
        )


class InvalidRequestDataError(BaseError):
    def __init__(self, errors):
        super(InvalidRequestDataError, self).__init__(
            'The submitted data does not meet the regulations',
            400,
            errors=errors
        )


@app.errorhandler(BaseError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
