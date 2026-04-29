import unittest
import json
import os

os.environ['FLASK_ENV'] = 'test'

from app import create_app
from app.core.extensions import db
from app.api.roles.models import Roles
from app.api.roles.seeds import seed_roles
from app.api.userProfile.models import UserProfile
from app.api.auth.models import Users


class UserProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            seed_roles()
            self.client.post('/api/auth/register', json={
                'username': 'testuser',
                'email': 'testuser@test.com',
                'password': 'password123'
            })
            login_res = self.client.post('/api/auth/login', json={
                'username': 'testuser',
                'password': 'password123'
            })
            data = json.loads(login_res.data)
            self.access_token = data['data']['access_token']
            self.user_id = 1

    def _auth_header(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            try:
                db.drop_all()
            except:
                pass

    def test_create_user_profile(self):
        res = self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe Smith',
            'telefono': '+1234567890',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertIn('data', data)
        self.assertEqual(data['data']['name'], 'John')

    def test_create_user_profile_duplicate(self):
        self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        res = self.client.post('/api/user-profile', json={
            'name': 'Jane',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        self.assertEqual(res.status_code, 400)

    def test_create_user_profile_missing_fields(self):
        res = self.client.post('/api/user-profile', json={
            'name': 'John'
        }, headers=self._auth_header())
        self.assertEqual(res.status_code, 400)

    def test_get_all_user_profiles(self):
        self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        res = self.client.get('/api/user-profile', headers=self._auth_header())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)

    def test_get_user_profile_by_id(self):
        self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        res = self.client.get('/api/user-profile/1', headers=self._auth_header())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'John')

    def test_get_user_profile_by_id_not_found(self):
        res = self.client.get('/api/user-profile/999', headers=self._auth_header())
        self.assertEqual(res.status_code, 404)

    def test_get_user_profile_by_user_id(self):
        self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        res = self.client.get(f'/api/user-profile/user/{self.user_id}', headers=self._auth_header())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'John')

    def test_get_user_profile_by_user_id_not_found(self):
        res = self.client.get('/api/user-profile/user/999', headers=self._auth_header())
        self.assertEqual(res.status_code, 404)

    def test_update_user_profile(self):
        self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        res = self.client.put('/api/user-profile/1', json={
            'name': 'Jane',
            'lastNames': 'Smith'
        }, headers=self._auth_header())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'Jane')

    def test_update_user_profile_not_found(self):
        res = self.client.put('/api/user-profile/999', json={
            'name': 'Jane'
        }, headers=self._auth_header())
        self.assertEqual(res.status_code, 404)

    def test_update_user_profile_invalid_rol(self):
        self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        res = self.client.put('/api/user-profile/1', json={
            'rolId': 999
        }, headers=self._auth_header())
        self.assertEqual(res.status_code, 400)

    def test_delete_user_profile(self):
        self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        }, headers=self._auth_header())
        res = self.client.delete('/api/user-profile/1', headers=self._auth_header())
        self.assertEqual(res.status_code, 200)

    def test_delete_user_profile_not_found(self):
        res = self.client.delete('/api/user-profile/999', headers=self._auth_header())
        self.assertEqual(res.status_code, 404)

    def test_create_user_profile_unauthorized(self):
        res = self.client.post('/api/user-profile', json={
            'name': 'John',
            'lastNames': 'Doe',
            'rolId': 1,
            'userId': self.user_id
        })
        self.assertEqual(res.status_code, 401)

    def test_get_all_user_profiles_unauthorized(self):
        res = self.client.get('/api/user-profile')
        self.assertEqual(res.status_code, 401)