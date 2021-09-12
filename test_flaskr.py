import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Drink, Role, setup_db_test

'Bearer Your_Token'
JWT_BARISTA = 'Bearer Your_Token'
JWT_MANAGER = 'Bearer Your_Token'
header_barista = {
    'Content-Type': 'application_json',
    'Authorization': JWT_BARISTA
}
header_manager = {
    'Content-Type': 'application_json',
    'Authorization': JWT_MANAGER
}

drink_barista = {
    'title': "milk",
    'recipe':
        {
            'name': "Milk",
            'color': "white",
            'parts': 1
        }
}

drink_manager = {
    'title': "matcha",
    'recipe':
        {
            'name': "Matcha",
            'color': "green",
            'parts': 1
        }
}

drink_unauthorized_user = {
    'title': "Lemon",
    'recipe':
        {
            'name': "Lemon",
            'color': "yellow",
            'parts': 1
        }
}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "coffee_shop_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db_test(self.app, self.database_path)

        self.new_drink = {
            'title': 'water',
            'created_by': 'Manager',
            'recipe': [
                {
                    "name": "water",
                    "color": "blue",
                    "parts": 1
                }
            ]
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # get drinks

    def test_get_drinks_as_barista(self):
        res = self.client().get('/drinks', headers=header_barista)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

    def test_get_drinks_as_manager(self):
        res = self.client().get('/drinks', headers=header_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

    def test_get_drinks_as_unauthorized_user(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # get drinks-detail
    def test_get_drinks_detail_as_barista(self):
        res = self.client().get('/drinks-detail', headers=header_barista)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_get_drinks_detail_as_manager(self):
        res = self.client().get('/drinks-detail', headers=header_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

    def test_get_drinks_detail_as_unauthorized_user(self):
        res = self.client().get('/drinks-detail')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # post drinks
    def test_post_drinks_as_barista(self):
        res = self.client().post('/drinks', headers=header_barista,
                                 json=drink_barista)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])
        self.assertEqual(data['drinks']['title'], drink_barista['title'])

    def test_post_drinks_as_manager(self):
        res = self.client().post('/drinks', headers=header_manager,
                                 json=drink_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])
        self.assertEqual(data['drinks']['title'], drink_manager['title'])

    def test_post_drinks_as_unauthorized_user(self):
        res = self.client().post('/drinks', json=drink_unauthorized_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # patch drinks
    def test_post_drinks_as_barista(self):
        res = self.client().patch('/drinks/1', headers=header_barista,
                                  json={'title': "Water"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_post_drinks_as_manager(self):
        res = self.client().patch('/drinks/1', headers=header_manager,
                                  json={'title': "Water"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])
        self.assertEqual(data['drinks'], ["Water"])

    def test_post_drinks_as_unauthorized_user(self):
        res = self.client().patch('/drinks/1',  json={'title': "Water"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # delete drinks
    def test_post_drinks_as_barista(self):
        res = self.client().delete('/drinks/1', headers=header_barista)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_post_drinks_as_manager(self):
        res = self.client().delete('/drinks/1', headers=header_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])
        self.assertEqual(data['delete'], 1)

    def test_post_drinks_as_unauthorized_user(self):
        res = self.client().delete('/drinks/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
