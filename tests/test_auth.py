import unittest
import json
import os
from datetime import datetime, timezone, timedelta
from app import create_app
from app.core.extensions import db
from app.api.auth.models import TokenBlocklist

class JWTAuthTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_app('test')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _get_tokens(self, username='testuser', password='password123'):
        login_res = self.client.post('/api/auth/login', json={
            'username': username,
            'password': password
        })
        data = json.loads(login_res.data)
        return data['data']['access_token'], data['data']['refresh_token']

    def test_register_and_login(self):
        res = self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(res.status_code, 201)

        res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(res.status_code, 200)
        
        data = json.loads(res.data)
        self.assertIn('access_token', data['data'])
        self.assertIn('refresh_token', data['data'])
        self.assertEqual(data['data']['expires_in'], 3600)

    def test_login_with_invalid_credentials(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'
        })
        
        res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertIn('Credenciales inválidas', data['message'])

    def test_login_nonexistent_user(self):
        res = self.client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'anypassword'
        })
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertIn('Credenciales inválidas', data['message'])

    def test_register_with_missing_fields(self):
        res = self.client.post('/api/auth/register', json={
            'username': 'testuser'
        })
        self.assertEqual(res.status_code, 400)
        
        res = self.client.post('/api/auth/register', json={
            'email': 'test@example.com'
        })
        self.assertEqual(res.status_code, 400)
        
        res = self.client.post('/api/auth/register', json={
            'password': 'password123'
        })
        self.assertEqual(res.status_code, 400)

    def test_register_duplicate_username(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test1@example.com', 'password': 'password123'
        })
        
        res = self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test2@example.com', 'password': 'password123'
        })
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('User already exists', data['message'])

    def test_register_duplicate_email(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser1', 'email': 'test@example.com', 'password': 'password123'
        })
        
        res = self.client.post('/api/auth/register', json={
            'username': 'testuser2', 'email': 'test@example.com', 'password': 'password123'
        })
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('User already exists', data['message'])

    def test_protected_route_without_token(self):
        res = self.client.get('/protected')
        self.assertEqual(res.status_code, 401)

    def test_protected_route_with_invalid_header_format(self):
        res = self.client.get('/protected', headers={
            'Authorization': 'InvalidFormat token123'
        })
        self.assertEqual(res.status_code, 401)

    def test_protected_route_with_token(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'
        })
        
        access_token, _ = self._get_tokens()
        
        res = self.client.get('/protected', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['user'], 'testuser')

    def test_access_after_logout(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@test.com', 'password': '123'
        })
        
        access_token, _ = self._get_tokens('testuser', '123')
        
        self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        
        res_protected = self.client.get('/protected', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res_protected.status_code, 401)

    def test_logout(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@test.com', 'password': '123'
        })
        
        access_token, _ = self._get_tokens('testuser', '123')
        
        res_logout = self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res_logout.status_code, 200)
        data = json.loads(res_logout.data)
        self.assertIn('Logout exitoso', data['message'])

    def test_double_logout(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@test.com', 'password': '123'
        })
        
        access_token, _ = self._get_tokens('testuser', '123')
        
        self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        
        res_second_logout = self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res_second_logout.status_code, 401)

    def test_keep_alive_without_token(self):
        res = self.client.post('/api/auth/keep-alive')
        self.assertEqual(res.status_code, 401)

    def test_keep_alive_with_valid_token(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@test.com', 'password': '123'
        })
        
        access_token, _ = self._get_tokens('testuser', '123')
        
        res = self.client.post('/api/auth/keep-alive', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res.status_code, 200)
        
        response_data = json.loads(res.data)
        self.assertTrue(response_data['data']['valid'])
        self.assertIn('expires_in', response_data['data'])
        self.assertFalse(response_data['data']['renewed'])

    def test_keep_alive_with_revoked_token(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@test.com', 'password': '123'
        })
        
        login_res = self.client.post('/api/auth/login', json={
            'username': 'testuser', 'password': '123'
        })
        login_data = json.loads(login_res.data)
        access_token = login_data['data']['access_token']
        
        logout_res = self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(logout_res.status_code, 200)
        
        res = self.client.post('/api/auth/keep-alive', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res.status_code, 401)

    def test_jwt_expired_token(self):
        """Verificar que token expirado devuelve 401"""
        from flask_jwt_extended import create_access_token
        
        with self.app.app_context():
            expired_token = create_access_token(
                identity='testuser',
                expires_delta=timedelta(seconds=-1)
            )
        
        res = self.client.get('/protected', headers={
            'Authorization': f'Bearer {expired_token}'
        })
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertIn('message', data)
        self.assertIn('Token expirado', data['message'])

if __name__ == '__main__':
    unittest.main()
