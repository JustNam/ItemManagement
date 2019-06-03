from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app import app
from models.category import Category
from models.item import Item
from utilities.message import error_message, message
from schemas.item import ItemSchema
from utilities.validate import convert_request_to_JSON, validate_by_schema


@app.route('/categories/<int:category_id>/items', methods=['GET'])
@jwt_required
def get_items_in_category(category_id):
    try:
        category = Category.check_existence(category_id)
    except ValidationError as e:
        return error_message(
            e.messages,
            400
        )

    items = [item.to_dict(['category', 'user']) for item in category.items]
    return jsonify(items)


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
@jwt_required
def get_item_in_category(category_id, item_id):
    # Check existences of category
    try:
        category = Category.check_existence(category_id)
    except ValidationError as e:
        return error_message(
            e.messages,
            400
        )
    item = category.items.filter_by(id=item_id).first()
    if not item:
        return error_message("Can not find the item with id = {} in the category".format(item_id), 400)
    return jsonify(item.to_dict(['category', 'user']))


@app.route('/categories/<int:category_id>/items', methods=['POST'])
@jwt_required
@validate_by_schema(ItemSchema)
def create_item_in_category(data, category_id):
    # Check existences of category
    try:
        Category.check_existence(category_id)
    except ValidationError as e:
        return error_message(
            e.messages,
            400
        )

    # Fill necessary fields
    data.user_id = get_jwt_identity()
    data.category_id = category_id

    # Check existences of item title
    try:
        Item.check_existence_of_title(data.title)
    except ValidationError as e:
        return error_message(
            'The submitted data does not meet the regulations',
            400,
            errors=e.messages
        )

    data.save_to_db()
    return message('Item "{}" was created.'.format(data.title))


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required
@validate_by_schema(ItemSchema)
def update_item_in_category(data, category_id, item_id):
    # Check existences of category and item
    try:
        category = Category.check_existence(category_id)
        item = category.check_existence_of_item(item_id)
    except ValidationError as e:
        return error_message(
            e.messages,
            400
        )

    # Check permission
    if item.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    # Save title of item for notification
    title = item.title

    # Check existences of item title
    try:
        Item.check_existence_of_title(data.title, item_id)
    except ValidationError as e:
        return error_message(
            'The submitted data does not meet the regulations',
            400,
            errors=e.messages
        )

    # Update final result
    item.update_from_copy(data)
    item.save_to_db()
    return message('Item "{}" was updated.'.format(title))


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def detele_item_in_category(category_id, item_id):
    # Check existences of category and item
    try:
        category = Category.check_existence(category_id)
        item = category.check_existence_of_item(item_id)
    except ValidationError as e:
        return error_message(
            e.messages,
            400
        )

    # Check permission
    if item.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    item.delete_from_db()
    return message('Item "{}" was deleted.'.format(item.title))
