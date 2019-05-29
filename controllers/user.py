from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app import app
from schemas.user import UserSchema
from utilities import message, error_message, generate_hash, verify_hash


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = UserSchema().load(data).data
    user.save_to_db()
    return message('Account with username "{}" was created.')


def login():
    if not request.is_json:
        return 'Missing JSON in request', 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return message('Missing username parameter', 400)
    if not password:
        return message('Missing password parameter', 400)

    if username != 'test' or password != 'test':
        return message('Invalid username or password', 401)

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


app.add_url_rule('/login', 'login', login, methods=['POST'])
