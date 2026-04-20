import unittest
import json
import os
from app import create_app


class CORSBlockedOriginsTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        os.environ['CORS_ORIGINS'] = 'http://localhost:3000,https://example.com'
        self.app = create_app('test')
        self.client = self.app.test_client()
    
    def test_unauthorized_origin_no_cors_headers(self):
        """Origin no permitido no debe incluir headers CORS"""
        res = self.client.get('/', headers={
            'Origin': 'http://malicious-site.com'
        })
        self.assertIsNone(res.headers.get('Access-Control-Allow-Origin'))
    
    def test_unauthorized_origin_get_request(self):
        """Origin no autorizado en GET debe tener acceso denegado"""
        res = self.client.get('/', headers={
            'Origin': 'http://hacker.org'
        })
        self.assertIsNone(res.headers.get('Access-Control-Allow-Origin'))
        self.assertEqual(res.status_code, 200)
    
    def test_unauthorized_origin_post_request(self):
        """Origin no autorizado en POST debe tener acceso denegado"""
        res = self.client.post('/api/auth/login', json={}, headers={
            'Origin': 'http://malicious.com'
        })
        self.assertIsNone(res.headers.get('Access-Control-Allow-Origin'))
    
    def test_invalid_origin_rejected(self):
        """Origin inválido no debe tener headers CORS"""
        res = self.client.get('/', headers={
            'Origin': 'not-a-valid-url'
        })
        self.assertIsNone(res.headers.get('Access-Control-Allow-Origin'))
    
    def test_multiple_unauthorized_origins(self):
        """Múltiples orígenes no autorizados no deben tener headers CORS"""
        unauthorized_origins = [
            'http://bad-site1.com',
            'http://bad-site2.com',
            'https://malicious.org',
            'http://phishing.net'
        ]
        
        for origin in unauthorized_origins:
            res = self.client.get('/', headers={'Origin': origin})
            self.assertIsNone(
                res.headers.get('Access-Control-Allow-Origin'),
                f"El origin {origin} no debería tener headers CORS"
            )


if __name__ == '__main__':
    unittest.main()