from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app import app
from models.user import User
from schemas.user import UserSchema
from utilities.message import message, error_message
from utilities.security import verify_hash
from utilities.validate import validate_by_schema, convert_request_to_JSON


@app.route('/users', methods=['POST'])
@validate_by_schema(UserSchema)
def create_user(data):
    old_user = User.find_by_username(data.username)
    if old_user:
        return error_message('The username "{}" already exists'.format(data.username), 400,
                             errors={
                                 'username': 'Account with username "{}" already exists.'.format(data.username)
                             })
    data.save_to_db()
    return message('Account with username "{}" was created.'.format(data.username))


@app.route('/login', methods=['POST'])
@validate_by_schema(UserSchema)
def login(data):
    # Because the password is hashed in post_load, this function have to achieve original information
    data = convert_request_to_JSON(request)
    user = User.find_by_username(data.get('username'))
    if not user:
        return error_message('Invalid username or password', 400)
    password = data.get('password')

    valid = verify_hash(password, user.password_hash)
    if not valid:
        return error_message('Invalid username or password', 400)

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
