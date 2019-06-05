from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app import app
from models.category import Category
from schemas.category import CategorySchema
from utilities.message import message, error_message
from utilities.validate import validate_by_schema


@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    results = [x.to_dict(relations=['user']) for x in categories]
    return jsonify(results)


@app.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required
def get_category(category_id):
    # Check existence of category
    try:
        category = Category.check_existence(category_id)
    except ValidationError as e:
        return error_message(e.messages, 404)
    return jsonify(category.to_dict(['user']))


@app.route('/categories', methods=['POST'])
@jwt_required
@validate_by_schema(CategorySchema)
def create_category(data):
    # Fill necessary field
    data.user_id = get_jwt_identity()

    # Check existences of category name
    try:
        Category.check_existence_of_name(data.name)
    except ValidationError as e:
        return error_message(
            'The submitted data does not meet the regulations',
            400,
            errors=e.messages,
        )
    data.save_to_db()
    return message('Category "{}" was created.'.format(data.name))


@app.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required
@validate_by_schema(CategorySchema)
def update_category(data, category_id):
    # Check existences of category
    try:
        category = Category.check_existence(category_id)
    except ValidationError as e:
        return error_message(e.messages, 404)

    # Check permission
    if category.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    # Fill necessary fields
    data.user_id = get_jwt_identity()

    # Save category name for notification
    name = category.name

    # Check existences of category name
    try:
        Category.check_existence_of_name(data.name, category_id)
    except ValidationError as e:
        return error_message(
            'The submitted data does not meet the regulations',
            400,
            errors=e.messages,
        )

    # Update final result
    category.update_from_copy(data)
    category.update_to_db()

    return message('Category "{}" was updated.'.format(name))


@app.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_category(category_id):
    # Check existences of category
    try:
        category = Category.check_existence(category_id)
    except ValidationError as e:
        return error_message(e.messages, 404)

    # Check permission
    if category.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    name = category.name
    category.delete_from_db()
    return message('Category "{}" was deleted'.format(name))
