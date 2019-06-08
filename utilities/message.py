from flask import jsonify


def message(text=None, code=200, data=None):
    if data:
        return jsonify(data)
    return jsonify(
        {
            'msg': text,
        }
    ), code
