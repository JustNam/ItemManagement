from flask import jsonify


def message(text=None, code=200, data=None):
    if data:
        return jsonify(data)
    return jsonify(
        {
            'msg': text,
        }
    ), code


def error_message(text, code, errors=None):
    return jsonify(
        {
            'msg': text,
            'errors': errors,
        }
    ), code


def record_not_found_error(model_name, id):
    """ Return a not found error which notifies that there is no requested record of the model in the database
    """
    return jsonify(
        {
            'msg': 'Can not find any {} with id = {}.'.format(model_name, id)
        }
    ), 404


def item_not_found_error(id):
    """ Return a not found error which notifies that there is no requested item in the category
    """
    return jsonify(
        {
            'msg': 'Can not find any item with id = {} in the category.'.format(id)
        }
    ), 404


def page_not_found_error():
    return jsonify(
        {
            'msg': 'Can not find the requested page.'
        }
    ), 404


def unique_value_error(model_name, field, value):
    return jsonify(
        {
            'msg': 'The submitted data does not meet the regulations',
            'errors': {
                field: '{} with {} = "{}" already exists.'.format(model_name, field, value)

            }
        }
    ), 400


def wrong_page_number_type_error():
    return jsonify(
        {
            'msg': 'The submitted parameter does not meet the regulations',
            'errors': {
                'page': [
                    "Not a valid integer."
                ]
            }
        }
    )


def forbidden_error():
    return error_message('You are not allowed to perform this action.', 403)


def pagination(current_page, last_page, items):
    return jsonify({
        'current_page': current_page,
        'last_page': last_page,
        'items': items
    })
