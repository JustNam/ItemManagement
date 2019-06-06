from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app
from models.category import Category
from schemas.category import CategorySchema
from utilities.message import message, record_not_found_error, unique_value_error, forbidden_error
from utilities.validate import validate_by_schema


@app.route('/categories', methods=['GET'])
@jwt_required
def get_categories():
    categories = Category.query.all()
    results = [x.to_dict(relations=['user']) for x in categories]
    return message(data=results)


@app.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required
def get_category(category_id):
    # Check existence of category
    category = Category.find_by_id(category_id)
    if not category:
        return record_not_found_error('category', category_id)
    return message(data=category.to_dict(relations=['user']))


@app.route('/categories', methods=['POST'])
@jwt_required
@validate_by_schema(CategorySchema)
def create_category(category):
    # Fill necessary field
    category.user_id = get_jwt_identity()

    # Check existence of category name
    name = category.name
    old_category = Category.find_by_name(name)
    if old_category:
        return unique_value_error('category', 'name', name)

    category.save_to_db()
    return message('Category "{}" was created.'.format(category.name))


@app.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required
@validate_by_schema(CategorySchema)
def update_category(new_category, category_id):
    # Check existence of category
    category = Category.find_by_id(category_id)
    if not category:
        return record_not_found_error('category', category_id)

    # Check permission
    if category.user.id != get_jwt_identity():
        return forbidden_error()

    # Save category name for notification
    new_name = new_category.name

    # Check existence of category name
    old_category = Category.find_by_name(new_name)
    if old_category and old_category.id != category_id:
        return unique_value_error('category', 'name', new_name)

    # Update final result
    category.update_from_copy(new_category)
    category.save_to_db()

    return message('Category "{}" was updated.'.format(new_name))


@app.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_category(category_id):
    # Check existence of category
    category = Category.find_by_id(category_id)
    if not category:
        return record_not_found_error('category', category_id)

    # Check permission
    if category.user.id != get_jwt_identity():
        return forbidden_error()

    name = category.name
    category.delete_from_db()
    return message('Category "{}" was deleted'.format(name))
