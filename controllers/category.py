from flask import request, jsonify

from app import app
from models.category import Category
from schemas.category import CategorySchema


def get_categories():
    # Have not finished yet
    categories = Category.query.all()


def create_category():
    # print(request.get_json())
    # category = Category().create_from_dict(request.get_json())
    # print(category.name)

    return jsonify({})


app.add_url_rule('/categories', 'create_category', create_category, methods=['POST'])
