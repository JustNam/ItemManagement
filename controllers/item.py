import math

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app
from models.category import Category
from models.item import Item
from utilities.message import (
    message, page_not_found_error, wrong_page_number_type_error, pagination,
    record_not_found_error, item_not_found_error, unique_value_error, forbidden_error
)
from schemas.item import ItemSchema
from utilities.validate import validate_by_schema


@app.route('/categories/<int:category_id>/items', methods=['GET'])
@jwt_required
def get_items_in_category(category_id):
    category = Category.find_by_id(category_id)
    if not category:
        return record_not_found_error('category', category_id)
    items = category.items

    page = request.args.get('page')
    if page:
        # Check if the page 'value' is integer
        try:
            page = int(page)
        except ValueError:
            return wrong_page_number_type_error()

        # Get index of last page, items
        number_of_items = items.count()
        number_of_records_in_page = app.config['NUMBER_OF_RECORDS_IN_ONE_PAGE']
        number_of_page = math.ceil(float(number_of_items) / number_of_records_in_page)
        if page < 1 or page > number_of_page:
            return page_not_found_error()
        offset = (page - 1) * number_of_records_in_page
        items = category.items.offset(offset).limit(number_of_records_in_page)
        items = [item.to_dict(relations=['user']) for item in items]
        return pagination(page, number_of_page, items)
    items = [item.to_dict(relations=['user']) for item in items]
    return message(data=items)


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
@jwt_required
def get_item_in_category(category_id, item_id):
    # Check existences of category and item
    category = Category.find_by_id(category_id)
    if not category:
        return record_not_found_error('category', category_id)
    item = category.items.filter_by(id=item_id).first()
    if not item:
        return item_not_found_error(item_id)
    return message(data=item.to_dict(relations=['category', 'user']))


@app.route('/categories/<int:category_id>/items', methods=['POST'])
@jwt_required
@validate_by_schema(ItemSchema)
def create_item_in_category(item, category_id):
    # Check existences of category
    category = Category.find_by_id(category_id)
    if not category:
        return record_not_found_error('category', category_id)

    # Fill necessary fields
    item.user_id = get_jwt_identity()
    item.category_id = category_id

    # Check existences of item title
    title = item.title
    old_item = Item.find_by_title(title)
    if old_item:
        return unique_value_error('item', 'title', title)

    item.save_to_db()
    return message('Item "{}" was created.'.format(item.title))


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required
@validate_by_schema(ItemSchema)
def update_item_in_category(new_item, category_id, item_id):
    # Check existences of category and item
    category = Category.find_by_id(category_id)
    if not category:
        return record_not_found_error('category', category_id)
    item = category.items.filter_by(id=item_id).first()
    if not item:
        return item_not_found_error(item_id)

    # Check permission
    if item.user.id != get_jwt_identity():
        return forbidden_error()

    # Save title of item for notification
    old_title = item.title

    # Check existences of item title
    title = new_item.title
    old_item = Item.find_by_title(title)
    if old_item and old_item.id != item_id:
        return unique_value_error('item', 'title', title)

    # Update final result
    item.update_from_copy(new_item)
    item.save_to_db()
    return message('Item "{}" was updated.'.format(old_title))


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_item_in_category(category_id, item_id):
    # Check existences of category and item
    category = Category.find_by_id(category_id)
    if not category:
        return record_not_found_error('category', category_id)
    item = category.items.filter_by(id=item_id).first()
    if not item:
        return item_not_found_error(item_id)

    # Check permission
    if item.user.id != get_jwt_identity():
        return forbidden_error()

    item.delete_from_db()
    return message('Item "{}" was deleted.'.format(item.title))
