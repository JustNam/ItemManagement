from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app import app
from models.category import Category
from models.item import Item
from utilities.message import error_message, message
from schemas.item import ItemSchema


@app.route('/categories/<int:category_id>/items', methods=['GET'])
@jwt_required
def get_items_in_category(category_id):
    print(request.is_json)
    category = Category.find_by_id(category_id)
    if not category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    items = [item.to_dict(['category', 'user']) for item in category.items]
    return jsonify(items)


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
@jwt_required
def get_item_in_category(category_id, item_id):
    # Check existences of category and item
    category = Category.find_by_id(category_id)
    if not category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    item = category.items.filter_by(id=item_id).first()
    if not item:
        return error_message("Can not find the item with id = {} in the category".format(item_id), 400)
    return jsonify(item.to_dict(['category', 'user']))


@app.route('/categories/<int:category_id>/items', methods=['POST'])
@jwt_required
def create_item_in_category(category_id):
    # Check existence of category
    category = Category.find_by_id(category_id)
    if not category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    # Fill necessary fields
    data = request.get_json()
    data['user_id'] = get_jwt_identity()
    data['category_id'] = category_id

    # Try converting data to Item model
    try:
        item = ItemSchema().load(data).data
    except ValidationError as e:
        return error_message('Item information do not meet regulations',
                             400,
                             errors=e.messages)

    # Check existences of item title
    old_item = Item.find_by_title(item.title)
    if old_item:
        return error_message('The title "{}" already exists.'.format(old_item.title),
                             400,
                             errors={
                                 'title': 'Item with title "{}" already exists.'.format(old_item.title)
                             })

    item.save_to_db()
    return message('Item "{}" was created.'.format(item.title))


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required
def update_item_in_category(category_id, item_id):
    # Check existences of category and item
    category = Category.find_by_id(category_id)
    if not category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    item = category.items.filter_by(id=item_id).first()
    if not item:
        return error_message("Can not find the item with id = {} in the category".format(item_id), 400)

    # Check permission
    if item.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    # Fill necessary fields
    data = request.get_json()
    data['user_id'] = get_jwt_identity()
    data['category_id'] = category_id

    # Save title of item for notification
    title = item.title

    # Try converting data to Item model
    try:
        ItemSchema().load(data)
    except ValidationError as e:
        return error_message('Item information do not meet regulations',
                             400,
                             errors=e.messages)

    # Check existences of item title
    if Item.find_by_title(data['title']):
        return error_message('The title "{}" already exists.'.format(data['title']),
                             400,
                             errors={
                                 'title': 'Item with title "{}" already exists.'.format(data['title'])
                             })

    # Update final result
    item.update_from_dict(data)
    item.save_to_db()
    return message('Item "{}" was updated.'.format(title))


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def detele_item_in_category(category_id, item_id):
    # Check existences of category and item
    category = Category.find_by_id(category_id)
    if not category:
        return error_message('Can not find any category with id = "{}"'.format(category_id), 404)

    item = category.items.filter_by(id=item_id).first()
    if not item:
        return error_message("Can not find the item with id = {} in the category".format(item_id), 400)

    # Check permission
    if item.user.id != get_jwt_identity():
        return error_message('You are not allowed to perform this action.', 403)

    item.delete_from_db()
    return message('Item "{}" was deleted.'.format(item.title))
