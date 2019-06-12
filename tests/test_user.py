import unittest
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from models.user import User
from schemas.user import UserSchema


class UserEndpointsTest(unittest.TestCase):
    def test_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username='nam123', password='nam123')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'access_token', response.data)

    def test_login_with_incorrect_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username='nam12334', password='nam123')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid username or password', response.data)

    def test_login_with_incorrect_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username='nam123', password='nam12345')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid username or password', response.data)

    def test_login_without_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(password='nam12345')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('username' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Missing data for required field.', response.data)

    def test_login_without_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username='nam123')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('password' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Missing data for required field.', response.data)

    def test_login_with_wrong_username_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username=1, password='nam12345')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('username' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Not a valid string.', response.data)

    def test_login_with_wrong_password_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username='nam123', password=1)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('password' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Not a valid string.', response.data)

    def test_login_with_wrong_content_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username='nam123', password=1))
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'"Content-type must be \\"application/json\\""', response.data)

    def test_login_with_wrong_JSON_format(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data='{"username":}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'"Wrong JSON format."', response.data)

    def test_register(self):
        tester = app.test_client(self)
        username = 'nam123456'
        response = tester.post(
            '/users',
            data=json.dumps(dict(username=username, password='nam123')),
            content_type='application/json'
        )
        test_user = User.find_by_username(username)
        test_user.delete_from_db()
        result = 'Account with username \\"{}\\" was created.'.format(username)
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes(result), response.data)

    def test_register_without_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(password='nam123')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('username' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Missing data for required field.', response.data)

    def test_register_without_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username='nam123')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('password' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Missing data for required field.', response.data)

    def test_register_with_wrong_type_of_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username=1, password='nam12345')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('username' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Not a valid string.', response.data)

    def test_register_with_wrong_type_of_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username='nam123', password=1)),
            content_type='application/json'
        )
        assert ('password' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Not a valid string.', response.data)

    def test_register_with_wrong_content_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username='nam123', password='nam123'))
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'"Content-type must be \\"application/json\\""', response.data)

    def test_register_with_wrong_JSON_format(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data='{"username":}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'"Wrong JSON format."', response.data)

    def test_register_with_existing_name(self):
        tester = app.test_client(self)
        username = 'duplicate'
        test_user = UserSchema().load({
            'username': username,
            'password': 'nam123'
        }).data
        test_user.save_to_db()
        response = tester.post(
            '/users',
            data=json.dumps(dict(username=username, password='nam123')),
            content_type='application/json'
        )
        test_user.delete_from_db()
        self.assertEqual(response.status_code, 400)
        assert ('username' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'user with username = \\"{}\\" already exists.'.format(username), response.data)

    def test_register_with_invalid_length_of_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username='na34', password='nam123')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('username' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Username must contain 6 to 30 characters.', response.data)

    def test_register_with_wrong_character_in_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username='_dafadfna34', password='nam123')),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert ('username' in json.loads(response.data.decode('utf-8'))['errors'])
        self.assertIn(b'Username must contain only lowercase letters, numbers.', response.data)


if __name__ == '__main__':
    unittest.main()
