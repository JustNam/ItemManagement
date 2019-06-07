import unittest
import json
import os
import sys

from flask_jwt_extended import create_access_token

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from models.item import Item
from models.category import Category


class ItemEndpointsTest(unittest.TestCase):
    # 'Get an item' endpoint
    def test_get_a_item(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/2/items/11', headers=headers)
            self.assertEqual(response.status_code, 200)
            assert ('created_on' in json.loads(response.data.decode('utf-8')))

    def test_create_an_item_with_wrong_category_id(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            category_id = 20

            result = 'Can not find any category with id = {}'.format(category_id)
            response = tester.post('/categories/{}/items'.format(category_id),
                                   data=json.dumps(dict(title="Sporty")),
                                   headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes(result), response.data)

    def test_get_a_item_without_authorization_header(self):
        tester = app.test_client(self)
        with app.app_context():
            response = tester.get('/categories/2/items/11')
            self.assertEqual(response.status_code, 401)
            self.assertIn(b'Missing Authorization Header', response.data)

    def test_get_a_item_with_expired_authorization_header(self):
        tester = app.test_client(self)
        with app.app_context():
            # Change expiration time
            app.config['JWT_ACCESS_TOKEN_EXPIRES'] = -1
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/2/items/11', headers=headers)
            app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 5
            self.assertEqual(response.status_code, 401)
            self.assertIn(b'Token has expired', response.data)

    def test_get_a_item_with_invalid_id_category(self):
        tester = app.test_client(self)
        with app.app_context():
            # Change expiration time back
            item_id = 11
            category_id = 200
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/{}/items/{}'.format(category_id, item_id),
                                  headers=headers)

            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes('Can not find any category with id = {}'
                                .format(category_id)),
                          response.data)

    def test_get_a_item_with_invalid_id_item(self):
        tester = app.test_client(self)
        with app.app_context():
            # Change expiration time back
            item_id = 111
            category_id = 2
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/{}/items/{}'.format(category_id, item_id),
                                  headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes('Can not find any item with id = {} in the category.'
                                .format(item_id)),
                          response.data)

    # 'Get all items' endpoint
    def test_get_all_items_in_category(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/2/items', headers=headers)
            self.assertEqual(response.status_code, 200)
            assert ('created_on' in json.loads(response.data.decode('utf-8'))[0])

    def test_get_all_items_in_category_with_pagination(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/2/items?page=1', headers=headers)
            self.assertEqual(response.status_code, 200)
            assert ('current_page' in json.loads(response.data.decode('utf-8')))

    def test_get_all_items_in_category_with_invalid_page(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/2/items?page=-1', headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Can not find the requested page.', response.data)

    def test_get_all_items_in_category_with_wrong_type_of_page_number(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            response = tester.get('/categories/2/items?page=a', headers=headers)
            self.assertEqual(response.status_code, 400)
            assert ('page' in json.loads(response.data.decode('utf-8'))['errors'])
            self.assertIn(b'Not a valid integer.', response.data)

    # 'Create an item' endpoint
    def test_create_a_item_in_category(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories/2/items',
                                   data=json.dumps(dict(title="whatever3")),
                                   headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'was created', response.data)

    def test_create_an_item_without_content_type(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }

            response = tester.post('/categories/2/items',
                                   data=json.dumps(dict(title="whatever")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Content-type must be \\"application/json\\"', response.data)

    def test_create_an_item_with_wrong_JSON_format(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories/2/items',
                                   data='{"title":}',
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Wrong JSON format.', response.data)

    def test_create_an_item_with_wrong_character_in_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories/2/items',
                                   data=json.dumps(dict(title="_nam123")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Item title must contain only lowercase letters', response.data)

    def test_create_an_item_with_invalid_length_of_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories/2/items',
                                   data=json.dumps(dict(title="nam123nam123nam123nam123nam123nam123nam123")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Item title must contain 1 to 30 characters.', response.data)

    def test_create_an_item_with_wrong_position_of_space_character(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories/2/items',
                                   data=json.dumps(dict(title=" nam123")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Item title must not start or end with space.', response.data)

    def test_create_an_item_with_continuous_spaces_in_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            response = tester.post('/categories/2/items',
                                   data=json.dumps(dict(title="nam  123")),
                                   headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Item title must not contain 2 continuous spaces.', response.data)

    def test_create_an_item_with_existing_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            title = "Skating shoe"
            response = tester.post('/categories/2/items',
                                   data=json.dumps(dict(title=title)),
                                   headers=headers)
            result = 'item with title = \\"{}\\" already exists.'.format(title)
            self.assertEqual(response.status_code, 400)
            self.assertIn(bytes(result), response.data)

    def test_create_an_item_with_wrong_type_of_name(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.post('/categories/2/items',
                                   data=json.dumps(dict(title=1)),
                                   headers=headers)
            assert ('title' in json.loads(response.data.decode('utf-8'))['errors'])
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Not a valid string.', response.data)

    # 'Update an item' endpoint
    def test_update_an_item(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            title = "Sporty"
            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title=title)),
                                  headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'was updated.', response.data)

    def test_update_an_item_without_content_type(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }

            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title="Sporty")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Content-type must be \\"application/json\\"', response.data)

    def test_update_an_item_with_wrong_JSON_format(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2/items/11',
                                  data='{"title":}',
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Wrong JSON format.', response.data)

    def test_update_an_item_with_wrong_character_in_title(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title="_nam123")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Item title must contain only lowercase letters', response.data)

    def test_update_an_item_with_invalid_length_of_title(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title="nam123nam123nam123nam123nam123nam123nam123")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Item title must contain 1 to 30 characters.', response.data)

    def test_update_an_item_with_wrong_position_of_space_character(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title=" nam123")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Item title must not start or end with space.', response.data)

    def test_update_an_item_with_continuous_spaces_in_title(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title="nam  123")),
                                  headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Item title must not contain 2 continuous spaces.', response.data)

    def test_update_an_item_with_existing_title(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            title = "Skating shoe"
            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title=title)),
                                  headers=headers)
            result = 'item with title = \\"{}\\" already exists.'.format(title)
            self.assertEqual(response.status_code, 400)
            self.assertIn(bytes(result), response.data)

    def test_update_an_item_with_wrong_type_of_title(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title=1)),
                                  headers=headers)
            assert ('title' in json.loads(response.data.decode('utf-8'))['errors'])
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Not a valid string.', response.data)

    def test_update_an_item_with_wrong_item_id(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            category_id = 2
            item_id = 200
            result = 'Can not find any item with id = {} in the category.'.format(item_id)
            response = tester.put('/categories/{}/items/{}'.format(category_id, item_id),
                                  data=json.dumps(dict(title="Sporty")),
                                  headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes(result), response.data)

    def test_update_an_item_with_wrong_category_id(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }
            category_id = 20
            item_id = 11

            result = 'Can not find any category with id = {}'.format(category_id)
            response = tester.put('/categories/{}/items/{}'.format(category_id, item_id),
                                  data=json.dumps(dict(title="Sporty")),
                                  headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes(result), response.data)

    def test_update_an_item_with_another_author(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(2)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-type': 'application/json',
            }

            response = tester.put('/categories/2/items/11',
                                  data=json.dumps(dict(title="Sporty")),
                                  headers=headers)
            self.assertEqual(response.status_code, 403)
            self.assertIn(b'You are not allowed to perform this action.', response.data)

    # 'Delete an item'
    def test_delete_an_item(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            category_id = 2
            category = Category.find_by_id(2)
            # items = category.items[len(category.items)-1]
            item_id = category.items.order_by(Item.id.desc()).first().id
            item = Item.find_by_id(item_id)
            result = 'Item \\"{}\\" was deleted.'.format(item.title)
            response = tester.delete('/categories/{}/items/{}'.format(category_id, item_id), headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn(bytes(result), response.data)

    def test_delete_an_item_with_another_author(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(2)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            category_id = 2
            item_id = 14
            response = tester.delete('/categories/{}/items/{}'.format(category_id, item_id), headers=headers)
            self.assertEqual(response.status_code, 403)
            self.assertIn(b'You are not allowed to perform this action.', response.data)

    def test_delete_an_item_with_wrong_id_category(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            category_id = 200
            item_id = 11
            result = 'Can not find any category with id = {}'.format(category_id)
            response = tester.delete('/categories/{}/items/{}'.
                                     format(category_id, item_id),
                                     headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes(result), response.data)

    def test_delete_an_item_with_wrong_id_item(self):
        tester = app.test_client(self)
        with app.app_context():
            access_token = create_access_token(1)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
            }
            category_id = 2
            item_id = 200
            result = 'Can not find any item with id = {} in the category.'.format(item_id)
            response = tester.delete('/categories/{}/items/{}'.
                                     format(category_id, item_id),
                                     headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(bytes(result), response.data)


if __name__ == '__main__':
    unittest.main()
