import unittest
import json
import os
from app import create_app


class CORSAllowedOriginsTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        os.environ['CORS_ORIGINS'] = 'http://localhost:3000,https://example.com'
        self.app = create_app('test')
        self.client = self.app.test_client()
        
    def test_cors_headers_present_on_get(self):
        """Verificar headers CORS en respuestas GET"""
        res = self.client.get('/')
        self.assertIn('Access-Control-Allow-Origin', res.headers)
        
    def test_cors_headers_present_on_post(self):
        """Verificar headers CORS en respuestas POST"""
        res = self.client.post('/api/auth/login', json={})
        self.assertIn('Access-Control-Allow-Origin', res.headers)
        
    def test_cors_headers_on_preflight_options(self):
        """Verificar respuesta a preflight OPTIONS"""
        res = self.client.options('/api/auth/login', headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Authorization,Content-Type'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('Access-Control-Allow-Methods', res.headers)
        self.assertIn('Access-Control-Allow-Headers', res.headers)
        
    def test_allow_credentials_header(self):
        """Verificar que Allow-Credentials esté presente"""
        res = self.client.get('/')
        self.assertEqual(res.headers.get('Access-Control-Allow-Credentials'), 'true')
        
    def test_allowed_methods_in_preflight(self):
        """Verificar métodos permitidos en preflight"""
        res = self.client.options('/api/auth/login', headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST'
        })
        allow_methods = res.headers.get('Access-Control-Allow-Methods', '')
        self.assertIn('POST', allow_methods)
        self.assertIn('OPTIONS', allow_methods)
        
    def test_max_age_header_present(self):
        """Verificar que Max-Age esté configurado"""
        res = self.client.options('/api/auth/login', headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST'
        })
        self.assertIn('Access-Control-Max-Age', res.headers)
        
    def test_allowed_headers_in_preflight(self):
        """Verificar headers permitidos en preflight"""
        res = self.client.options('/api/auth/login', headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Authorization,Content-Type'
        })
        allow_headers = res.headers.get('Access-Control-Allow-Headers', '')
        self.assertIn('Authorization', allow_headers)
        self.assertIn('Content-Type', allow_headers)
        
    def test_cors_with_allowed_origin(self):
        """Verificar CORS con origen permitido"""
        res = self.client.get('/', headers={
            'Origin': 'http://localhost:3000'
        })
        self.assertEqual(res.headers.get('Access-Control-Allow-Origin'), 
                        'http://localhost:3000')
        
    def test_cors_with_allowed_production_origin(self):
        """Verificar CORS con origen de producción"""
        res = self.client.get('/', headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(res.headers.get('Access-Control-Allow-Origin'),
                        'https://example.com')
        
    def test_origin_reflected_in_response(self):
        """Verificar que el Origin se refleje correctamente"""
        res = self.client.get('/', headers={
            'Origin': 'http://localhost:3000'
        })
        self.assertEqual(res.headers['Access-Control-Allow-Origin'], 
                        'http://localhost:3000')


if __name__ == '__main__':
    unittest.main()