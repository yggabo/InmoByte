import unittest
import json
import os
from datetime import timedelta
from app import create_app
from app.core.extensions import db


class JWTAuthHandlersTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_app('test')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
        
        self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
    
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
    
    def test_unauthorized_no_token(self):
        """Sin token debe retornar 401"""
        res = self.client.get('/protected')
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertIn('Token no proporcionado', data['message'])
    
    def test_invalid_token_format(self):
        """Token con formato inválido debe retornar 401"""
        res = self.client.get('/protected', headers={
            'Authorization': 'InvalidFormat token123'
        })
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertIn('Token', data['message'])
    
    def test_expired_token(self):
        """Token expirado debe retornar 401"""
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
        self.assertIn('Token expirado', data['message'])
    
    def test_revoked_token(self):
        """Token revocado debe retornar 401"""
        access_token, _ = self._get_tokens()
        
        self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        
        res = self.client.get('/protected', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertIn('Token revocado', data['message'])
    
    def test_valid_token(self):
        """Token válido debe permitir acceso"""
        access_token, _ = self._get_tokens()
        
        res = self.client.get('/protected', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['user'], 'testuser')
    
    def test_jwt_error_response_structure(self):
        """Error JWT debe tener estructura correcta"""
        res = self.client.get('/protected')
        data = json.loads(res.data)
        
        self.assertIn('message', data)
        self.assertIn('status_code', data)
        self.assertIn('error', data)
        self.assertEqual(data['status_code'], 401)
        self.assertEqual(data['error'], 'Unauthorized')
    
    def test_keep_alive_without_token(self):
        """Keep-alive sin token debe retornar 401"""
        res = self.client.post('/api/auth/keep-alive')
        self.assertEqual(res.status_code, 401)
    
    def test_keep_alive_with_valid_token(self):
        """Keep-alive con token válido debe retornar 200"""
        access_token, _ = self._get_tokens()
        
        res = self.client.post('/api/auth/keep-alive', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res.status_code, 200)
        
        response_data = json.loads(res.data)
        self.assertTrue(response_data['data']['valid'])
        self.assertIn('expires_in', response_data['data'])
    
    def test_logout_with_valid_token(self):
        """Logout con token válido debe funcionar"""
        access_token, _ = self._get_tokens()
        
        res = self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('Logout exitoso', data['message'])
    
    def test_double_logout(self):
        """Segundo logout con token ya revocado debe retornar 401"""
        access_token, _ = self._get_tokens()
        
        self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        
        res = self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()