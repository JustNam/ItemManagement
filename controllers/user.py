from flask import request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from marshmallow import ValidationError

from app import app
from schemas.user import UserSchema
from utilities.message import message, error_message
from utilities.security import verify_hash


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        user = UserSchema().load(data).data
    except ValidationError as e:
        return error_message("User information do not meet regulations",
                             400,
                             errors=e.messages)
    old_user = User.find_by_username(user.username)
    if old_user:
        return error_message('The username "{}" already exists'.format(user.username), 400,
                             errors={
                                 'username': 'Account with username "{}" already exists.'.format(user.username)
                             })
    user.save_to_db()
    return message('Account with username "{}" was created.'.format(user.username))


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return 'Content-type must be "application/json"', 400

    data = request.json
    user = User.find_by_username(data.get('username'))
    if not user:
        return error_message('Invalid username or password', 400)
    password = data.get('password')

    valid = verify_hash(password, user.password_hash)

    if not valid:
        return error_message('Invalid username or password', 400)

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
