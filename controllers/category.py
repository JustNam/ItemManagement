from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app import app
from models.category import Category
from schemas.category import CategorySchema
from utilities.message import message, error_message
from utilities.validate import convert_request_to_JSON


@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    results = [x.to_dict(relations=['user']) for x in categories]
    return jsonify(results)


@app.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required
def get_category(category_id):

    # Check existence of category
    category = Category.find_by_id(category_id)
    if not category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)
    return jsonify(category.to_dict(['user']))


@app.route('/categories', methods=['POST'])
@jwt_required
def create_category():
    # Fill necessary fields
    try:
        data = convert_request_to_JSON(request)
    except ValidationError as e:
        return error_message(e.messages[0], 400)
    data['user_id'] = get_jwt_identity()

    # Try converting data to Category model
    try:
        category = CategorySchema().load(data).data
    except ValidationError as e:
        return error_message('Category information do not meet regulations',
                             400,
                             errors=e.messages)

    # Check existences of category name
    old_category = Category.find_by_name(category.name)
    if old_category:
        return error_message('The name "{}" already exists'.format(category.name), 400,
                             errors={
                                 'name': 'Category with name "{}" already exists.'.format(category.name)
                             })
    category.save_to_db()
    return message('Category "{}" was created.'.format(category.name))


@app.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required
def update_category(category_id):
    # Check existences of category and item
    category = Category.find_by_id(category_id)
    if not category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    # Check permission
    if category.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    # Fill necessary fields
    try:
        data = convert_request_to_JSON(request)
    except ValidationError as e:
        return error_message(e.messages[0], 400)
    data['user_id'] = get_jwt_identity()

    # Save category name for notification
    name = category.name

    # Try converting data to Category model
    try:
        CategorySchema().load(data)
    except ValidationError as e:
        return error_message("Category information do not meet regulations",
                             400,
                             errors=e.messages)

    # Check existences of category name
    if Category.find_by_name(data['name']):
        return error_message('The title "{}" already exists.'.format(data['name']),
                             400,
                             errors={
                                 'title': 'Item with title "{}" already exists.'.format(data['name'])
                             })
    # Update final result
    category.update_from_dict(data)
    category.update_to_db()

    return message('Category "{}" was updated.'.format(name))


@app.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_category(category_id):
    # Check existence of category
    category = Category.find_by_id(category_id)
    if not category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    # Check permission
    if category.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    name = category.name
    category.delete_from_db()
    return message('Category "{}" was deleted'.format(name))
