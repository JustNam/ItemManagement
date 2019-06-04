import unittest
import json
import os
import sys

from flask_jwt_extended import create_access_token

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from models.category import Category


class CategoryEndpointsTest(unittest.TestCase):
    # 'Get a category' endpoint
    def test_get_a_category(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            id = 2
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/{}'.format(id), headers=headers)
            self.assertEqual(response.status_code, 200)
            assert ('created_on' in json.loads(response.data.decode('utf-8')))

    def test_get_a_category_without_authorization_header(self):
        tester = app.test_client(self)
        with app.app_context():
            id = 2
            response = tester.get('/categories/{}'.format(id))
            self.assertEqual(response.status_code, 401)
            self.assertIn(b'Missing Authorization Header', response.data)

    def test_get_a_category_with_expired_authorization_header(self):
        tester = app.test_client(self)
        with app.app_context():
            # Change expiration time
            app.config['JWT_ACCESS_TOKEN_EXPIRES'] = -1
            id = 2
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/{}'.format(id), headers=headers)

            self.assertEqual(response.status_code, 401)
            self.assertIn(b'Token has expired', response.data)

    def test_get_a_category_with_invalid_id(self):
        tester = app.test_client(self)
        with app.app_context():
            # Change expiration time back
            app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 5
            id = 200
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/{}'.format(id), headers=headers)

            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Can not find any category with id', response.data)

    # 'Get all categories' endpoint
    def test_get_all_categories(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                # 'Content-type': 'application/json',
            }
            response = tester.get('/categories', headers=headers)
            self.assertEqual(response.status_code, 200)
            assert ('created_on' in json.loads(response.data.decode('utf-8'))[0])

    # 'Create a category' endpoint
    def test_create_a_category(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories',
                                   data=json.dumps(dict(name="whatever1")),
                                   headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'was created', response.data)

    def test_create_a_category_without_content_type(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }

            response = tester.post('/categories',
                                   data=json.dumps(dict(name="whatever")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Content-type must be \\"application/json\\"', response.data)

    def test_create_a_category_with_wrong_JSON_format(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories',
                                   data='{"name":}',
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Wrong JSON format.', response.data)

    def test_create_a_category_with_wrong_character_in_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories',
                                   data=json.dumps(dict(name="_nam123")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Category name must contain only lowercase letters', response.data)

    def test_create_a_category_with_invalid_length_of_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories',
                                   data=json.dumps(dict(name="nam123nam123nam123nam123nam123nam123nam123")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Category name must contain 1 to 30 characters.', response.data)

    def test_create_a_category_with_wrong_position_of_space_character(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories',
                                   data=json.dumps(dict(name=" nam123")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Category name must not start or end with space.', response.data)

    def test_create_a_category_with_continuous_spaces_in_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories',
                                   data=json.dumps(dict(name="nam  123")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Category name must not contain 2 continuous spaces.', response.data)

    def test_create_a_category_with_existing_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            name = Category.query.order_by(Category.id.desc()).first().name
            response = tester.post('/categories',
                                   data=json.dumps(dict(name=name)),
                                   headers=headers)
            result = 'Category with name \\"{}\\" already exists.'.format(name)
            self.assertEqual(response.status_code, 400)
            self.assertIn(bytes(result), response.data)

    def test_create_a_category_with_wrong_type_of_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories',
                                   data=json.dumps(dict(name=1)),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            assert ('name' in json.loads(response.data.decode('utf-8'))['errors'])
            self.assertIn(b'Not a valid string.', response.data)

    # 'Update a category' endpoint
    def test_update_a_category(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            name = "Climbing"
            result = 'Category \\"{}\\" was updated.'.format(name)
            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name=name)),
                                  headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'was updated.', response.data)

    def test_update_a_category_without_content_type(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }

            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name="Sporty")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Content-type must be \\"application/json\\"', response.data)

    def test_update_a_category_with_wrong_JSON_format(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2',
                                  data='{"name":}',
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Wrong JSON format.', response.data)

    def test_update_a_category_with_wrong_character_in_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name="_nam123")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Category name must contain only lowercase letters', response.data)

    def test_update_a_category_with_invalid_length_of_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name="nam123nam123nam123nam123nam123nam123nam123")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Category name must contain 1 to 30 characters.', response.data)

    def test_update_a_category_with_wrong_position_of_space_character(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name=" nam123")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Category name must not start or end with space.', response.data)

    def test_update_a_category_with_continuous_spaces_in_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name="nam  123")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Category name must not contain 2 continuous spaces.', response.data)

    def test_update_a_category_with_existing_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            name = Category.query.all()[0].name
            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name=name)),
                                  headers=headers)
            result = 'Category with name \\"{}\\" already exists.'.format(name)
            self.assertEqual(response.status_code, 400)
            self.assertIn(bytes(result), response.data)

    def test_update_a_category_with_wrong_type_of_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name=1)),
                                  headers=headers)
            assert ('name' in json.loads(response.data.decode('utf-8'))['errors'])
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Not a valid string.', response.data)

    def test_update_a_category_with_wrong_id(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            id = 200
            result = 'Can not find any category with id = {}'.format(id)
            response = tester.put('/categories/{}'.format(id),
                                  data=json.dumps(dict(name="Sporty")),
                                  headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes(result), response.data)

    def test_update_a_category_with_another_author(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(2)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2',
                                  data=json.dumps(dict(name="Sporty")),
                                  headers=headers)
            self.assertEqual(response.status_code, 403)
            self.assertIn(b'You are not allowed to perform this action.', response.data)

    # 'Delete a category'
    def test_delete_a_category(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            category = Category.query.order_by(Category.id.desc()).first()
            result = 'Category \\"{}\\" was deleted"'.format(category.name)
            response = tester.delete('/categories/{}'.format(category.id), headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn(bytes(result), response.data)

    def test_delete_a_category_with_another_author(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(2)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            category_id = Category.query.order_by(Category.id.desc()).first().id

            response = tester.delete('/categories/{}'.format(category_id), headers=headers)
            self.assertEqual(response.status_code, 403)
            self.assertIn(b'You are not allowed to perform this action.', response.data)

    def test_delete_a_category_with_wrong_id(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            id = 200
            result = 'Can not find any category with id = {}'.format(id)
            response = tester.delete('/categories/{}'.format(id), headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes(result), response.data)


if __name__ == '__main__':
    unittest.main()
