from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app import app
from models.category import Category
from schemas.category import CategorySchema
from utilities.message import message, error_message


@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    results = [x.to_dict(1) for x in categories]
    return jsonify(results)


@app.route('/categories', methods=['POST'])
@jwt_required
def create_category():
    data = request.get_json()
    data['user_id'] = get_jwt_identity()
    try:
        category = CategorySchema().load(data).data
    except ValidationError as e:
        return error_message("Category information do not meet regulations",
                             400,
                             errors=e.messages)
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
    data = request.get_json()

    old_category = Category.find_by_id(category_id)
    if not old_category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    print(old_category)
    if old_category.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    try:
        data['user_id'] = get_jwt_identity()
        CategorySchema().load(data)
    except ValidationError as e:
        return error_message("Category information do not meet regulations",
                             400,
                             errors=e.messages)

    old_category.update_from_dict(data)
    old_category.update_to_db()

    return message('Category "{}" was updated.'.format(old_category.name))


@app.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_category(category_id):
    old_category = Category.find_by_id(category_id)
    if not old_category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    print(old_category)
    print(get_jwt_identity())
    if old_category.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    name = old_category.name
    old_category.delete_from_db()
    return message('Category "{}" was deleted'.format(name))
