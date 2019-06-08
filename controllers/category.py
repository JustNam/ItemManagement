from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app
from models.category import Category
from schemas.category import CategorySchema
from utilities.message import message
from utilities.validate import validate_by_schema
from errors import RecordNotFoundError, DuplicateValueError, ForbiddenError


@app.route('/categories', methods=['GET'])
@jwt_required
def get_categories():
    categories = Category.query.all()
    categories = CategorySchema().dump(categories, many=True).data
    return message(data=categories)


@app.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required
def get_category(category_id):
    # Check existence of category
    category = Category.find_by_id(category_id)
    if not category:
        raise RecordNotFoundError('category', category_id)
    category = CategorySchema().dump(category).data
    return message(data=category)


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
        raise DuplicateValueError('category', 'name', name)

    category.save_to_db()
    return message('Category "{}" was created.'.format(category.name))


@app.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required
@validate_by_schema(CategorySchema)
def update_category(new_category, category_id):
    # Check existence of category
    category = Category.find_by_id(category_id)
    if not category:
        raise RecordNotFoundError('category', category_id)

    # Check permission
    if category.user.id != get_jwt_identity():
        raise ForbiddenError()

    # Save category name for notification
    new_name = new_category.name

    # Check existence of category name
    old_category = Category.find_by_name(new_name)
    if old_category and old_category.id != category_id:
        raise DuplicateValueError('category', 'name', new_name)

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
        raise RecordNotFoundError('category', category_id)

    # Check permission
    if category.user.id != get_jwt_identity():
        raise ForbiddenError()

    name = category.name
    category.delete_from_db()
    return message('Category "{}" was deleted'.format(name))
