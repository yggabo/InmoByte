import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.clients.models import Client


class PreferencesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self._seed_test_data()

        self._register_and_login()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _register_and_login(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        login_res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        data = json.loads(login_res.data)
        self.access_token = data['data']['access_token']

    def _auth_headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def _seed_test_data(self):
        with self.app.app_context():
            client = Client(name='John', email='john@example.com', phone='1234567890', address='123 Main St', age=30)
            db.session.add(client)
            db.session.commit()
            self.client_id = client.id

    def test_create_preferences(self):
        res = self.client.post('/api/preferences/', json={
            'client_id': self.client_id,
            'property_type_id': 1,
            'price_min': 100000,
            'price_max': 200000,
            'location': 'Madrid',
            'bedrooms': 3,
            'bathrooms': 2,
            'additional_features': {'garage': True, 'garden': False},
            'living_space_min': 80,
            'living_space_max': 120
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['client_id'], self.client_id)
        self.assertEqual(data['data']['location'], 'Madrid')

    def test_create_preferences_missing_fields(self):
        res = self.client.post('/api/preferences/', json={
            'client_id': self.client_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('Missing fields', data['message'])

    def test_create_preferences_duplicate(self):
        preferences_data = {
            'client_id': self.client_id,
            'property_type_id': 1,
            'price_min': 100000,
            'price_max': 200000,
            'location': 'Madrid',
            'bedrooms': 3,
            'bathrooms': 2,
            'additional_features': {'garage': True},
            'living_space_min': 80,
            'living_space_max': 120
        }

        res1 = self.client.post('/api/preferences/', json=preferences_data, headers=self._auth_headers())
        self.assertEqual(res1.status_code, 201)

        res2 = self.client.post('/api/preferences/', json=preferences_data, headers=self._auth_headers())
        self.assertEqual(res2.status_code, 409)

    def test_get_preferences(self):
        self.client.post('/api/preferences/', json={
            'client_id': self.client_id,
            'property_type_id': 1,
            'price_min': 100000,
            'price_max': 200000,
            'location': 'Madrid',
            'bedrooms': 3,
            'bathrooms': 2,
            'additional_features': {'garage': True},
            'living_space_min': 80,
            'living_space_max': 120
        }, headers=self._auth_headers())

        res = self.client.get(f'/api/preferences/{self.client_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['client_id'], self.client_id)

    def test_get_preferences_not_found(self):
        res = self.client.get('/api/preferences/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_update_preferences(self):
        self.client.post('/api/preferences/', json={
            'client_id': self.client_id,
            'property_type_id': 1,
            'price_min': 100000,
            'price_max': 200000,
            'location': 'Madrid',
            'bedrooms': 3,
            'bathrooms': 2,
            'additional_features': {'garage': True},
            'living_space_min': 80,
            'living_space_max': 120
        }, headers=self._auth_headers())

        res = self.client.put(f'/api/preferences/{self.client_id}', json={
            'location': 'Barcelona',
            'price_max': 250000
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['location'], 'Barcelona')
        self.assertEqual(data['data']['price_max'], 250000)

    def test_update_preferences_not_found(self):
        res = self.client.put('/api/preferences/9999', json={
            'location': 'Barcelona'
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 404)

    def test_update_preferences_no_data(self):
        self.client.post('/api/preferences/', json={
            'client_id': self.client_id,
            'property_type_id': 1,
            'price_min': 100000,
            'price_max': 200000,
            'location': 'Madrid',
            'bedrooms': 3,
            'bathrooms': 2,
            'additional_features': {'garage': True},
            'living_space_min': 80,
            'living_space_max': 120
        }, headers=self._auth_headers())

        res = self.client.put(f'/api/preferences/{self.client_id}', json={}, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)

    def test_create_preferences_without_token(self):
        res = self.client.post('/api/preferences/', json={
            'client_id': self.client_id,
            'property_type_id': 1,
            'price_min': 100000,
            'price_max': 200000,
            'location': 'Madrid',
            'bedrooms': 3,
            'bathrooms': 2,
            'additional_features': {},
            'living_space_min': 80,
            'living_space_max': 120
        })

        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
