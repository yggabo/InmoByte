import unittest
import json
import os
from app import create_app
from app.core.extensions import db


class CORSIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        os.environ['CORS_ORIGINS'] = 'http://localhost:3000'
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
    
    def test_frontend_get_request(self):
        """Simular request GET desde frontend (localhost:3000)"""
        res = self.client.get('/', headers={
            'Origin': 'http://localhost:3000'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get('Access-Control-Allow-Origin'), 
                        'http://localhost:3000')
        self.assertEqual(res.headers.get('Access-Control-Allow-Credentials'), 'true')
    
    def test_frontend_post_request(self):
        """Simular request POST desde frontend"""
        res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        }, headers={
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        })
        self.assertIn('Access-Control-Allow-Origin', res.headers)
        self.assertEqual(res.headers.get('Access-Control-Allow-Origin'),
                        'http://localhost:3000')
        self.assertEqual(res.status_code, 200)
        
        data = json.loads(res.data)
        self.assertIn('data', data)
        self.assertIn('access_token', data['data'])
    
    def test_preflight_from_frontend(self):
        """Simular request OPTIONS (preflight) desde frontend"""
        res = self.client.options('/', headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Authorization,Content-Type'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('Access-Control-Allow-Origin', res.headers)
        self.assertIn('Access-Control-Allow-Methods', res.headers)
        self.assertIn('Access-Control-Allow-Headers', res.headers)
        self.assertIn('Access-Control-Max-Age', res.headers)
    
    def test_frontend_protected_request(self):
        """Request a ruta protegida con token válido desde frontend"""
        login_res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        }, headers={'Origin': 'http://localhost:3000'})
        
        data = json.loads(login_res.data)
        access_token = data['data']['access_token']
        
        res = self.client.get('/protected', headers={
            'Authorization': f'Bearer {access_token}',
            'Origin': 'http://localhost:3000'
        })
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('Access-Control-Allow-Origin', res.headers)
    
    def test_frontend_preflight_login(self):
        """Preflight para login desde frontend"""
        res = self.client.options('/api/auth/login', headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Authorization,Content-Type'
        })
        
        self.assertEqual(res.status_code, 200)
        allow_origin = res.headers.get('Access-Control-Allow-Origin')
        allow_methods = res.headers.get('Access-Control-Allow-Methods')
        allow_headers = res.headers.get('Access-Control-Allow-Headers')
        
        self.assertEqual(allow_origin, 'http://localhost:3000')
        self.assertIn('POST', allow_methods)
        self.assertIn('OPTIONS', allow_methods)
        self.assertIn('Authorization', allow_headers)
    
    def test_frontend_without_origin(self):
        """Request sin origin debe funcionar (no CORS)"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
    
    def test_frontend_logout_request(self):
        """Request de logout desde frontend"""
        login_res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        }, headers={'Origin': 'http://localhost:3000'})
        
        data = json.loads(login_res.data)
        access_token = data['data']['access_token']
        
        res = self.client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}',
            'Origin': 'http://localhost:3000'
        })
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('Access-Control-Allow-Origin', res.headers)


if __name__ == '__main__':
    unittest.main()