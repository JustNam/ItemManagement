import unittest
import json
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app


class UserEndpointsTest(unittest.TestCase):
    def test_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username="nam123", password="nam123")),
            content_type='application/json'
        )
        # assert b'access_token' in response.data
        self.assertIn(b'access_token', response.data)

    def test_login_with_incorrect_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username="nam12334", password="nam123")),
            content_type='application/json'
        )
        self.assertIn(b'Invalid username or password', response.data)

    def test_login_with_incorrect_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username="nam123", password="nam12345")),
            content_type='application/json'
        )
        self.assertIn(b'Invalid username or password', response.data)

    def test_login_without_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(password="nam12345")),
            content_type='application/json'
        )
        self.assertIn(b'"username":["Missing data for required field."]', response.data)

    def test_login_without_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username="nam123")),
            content_type='application/json'
        )
        self.assertIn(b'"password":["Missing data for required field."]', response.data)

    def test_login_with_wrong_username_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username=1, password="nam12345")),
            content_type='application/json'
        )
        self.assertIn(b'"username":["Not a valid string."', response.data)

    def test_login_with_wrong_password_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username="nam123", password=1)),
            content_type='application/json'
        )
        self.assertIn(b'"password":["Not a valid string."', response.data)

    def test_login_with_wrong_content_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=json.dumps(dict(username="nam123", password=1))
        )
        self.assertIn(b'"Content-type must be \\"application/json\\""', response.data)

    def test_login_with_wrong_JSON_format(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data='{"username":}',
            content_type='application/json'
        )
        self.assertIn(b'"Wrong JSON format."', response.data)

    def test_register(self):
        tester = app.test_client(self)
        username = "nam123456"
        response = tester.post(
            '/users',
            data=json.dumps(dict(username=username, password="nam123")),
            content_type='application/json'
        )
        result = 'Account with username \\"{}\\" was created.'.format(username)
        self.assertIn(bytes(result, 'utf8'), response.data)

    def test_register_without_username(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(password="nam123")),
            content_type='application/json'
        )
        self.assertIn(b'"username":["Missing data for required field."]', response.data)

    def test_register_without_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username="nam123")),
            content_type='application/json'
        )
        self.assertIn(b'"password":["Missing data for required field."]', response.data)

    def test_register_with_wrong_username_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username=1, password="nam12345")),
            content_type='application/json'
        )
        self.assertIn(b'"username":["Not a valid string."', response.data)

    def test_register_with_wrong_password_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username="nam123", password=1)),
            content_type='application/json'
        )
        self.assertIn(b'"password":["Not a valid string."', response.data)

    def test_register_with_wrong_content_type(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username="nam123", password="NAM123"))
        )
        self.assertIn(b'"Content-type must be \\"application/json\\""', response.data)

    def test_register_with_wrong_JSON_format(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data='{"username":}',
            content_type='application/json'
        )
        self.assertIn(b'"Wrong JSON format."', response.data)

    def test_register_with_existing_name(self):
        tester = app.test_client(self)
        response = tester.post(
            '/users',
            data=json.dumps(dict(username="nam123", password="nam123")),
            content_type='application/json'
        )
        self.assertIn(b'"The username \\"nam123\\" already exists"', response.data)


if __name__ == '__main__':
    unittest.main()
