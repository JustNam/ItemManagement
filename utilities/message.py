from flask import jsonify


def error_message(text, code, errors={}):
    return jsonify(
        {
            'msg': text,
            'errors': errors,
        }
    ), code


def message(text, code=200):
    return jsonify(
        {
            'msg': text,
        }
    ), code
