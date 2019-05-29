import re

from flask import jsonify
from passlib.hash import pbkdf2_sha256 as sha256


def error_message(text, code, errors=None):
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


def convert_column_to_string(column):
    return re.sub(r'.*\.', '', str(column))


def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, hash):
    return sha256.verify(password, hash)
