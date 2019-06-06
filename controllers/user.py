from flask_jwt_extended import create_access_token

from app import app
from models.user import User
from schemas.user import UserSchema
from utilities.message import message, error_message, unique_value_error
from utilities.security import verify_hash
from utilities.validate import validate_by_schema


@app.route('/users', methods=['POST'])
@validate_by_schema(UserSchema)
def create_user(user):
    old_user = User.find_by_username(user.username)
    if old_user:
        return unique_value_error('user', 'username', user.username)
    user.save_to_db()
    return message('Account with username "{}" was created.'.format(user.username))


@app.route('/login', methods=['POST'])
@validate_by_schema(UserSchema)
def login(user):
    # Because the password is hashed in post_load, this function have to achieve original information
    user_in_db = User.find_by_username(user.username)
    if not user_in_db:
        return error_message('Invalid username or password', 400)
    password = user.password

    valid = verify_hash(password, user_in_db.password_hash)
    if not valid:
        return error_message('Invalid username or password', 400)

    access_token = create_access_token(identity=user_in_db.id)
    return message(data={'access_token': access_token})
