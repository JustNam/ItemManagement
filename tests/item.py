from flask_jwt_extended import create_access_token

import unittest
import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app


class ItemEndpointsTest(unittest.TestCase):
    def test_get(self):
        tester = app.test_client(self)
        access_token = create_access_token(1)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            # 'Content-type': 'application/json',
        }
        response = tester.get('/foo', headers=headers)

        # assert b'access_token' in response.data
        self.assertIn(b'access_token', response.data)
