import unittest
import json
import os
from app import create_app

class ErrorHandlingTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_app('test')
        self.client = self.app.test_client()
        
    def test_404_returns_json(self):
        """Verificar que 404 devuelve JSON"""
        res = self.client.get('/ruta-inexistente')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 404)
        self.assertIn('message', data)
        self.assertIn('error', data)
        
    def test_404_message_content(self):
        """Verificar mensaje de error 404"""
        res = self.client.get('/no-existe')
        data = json.loads(res.data)
        self.assertIn('Ruta no encontrada', data['message'])
        
    def test_405_returns_json(self):
        """Verificar que 405 devuelve JSON"""
        res = self.client.patch('/')
        self.assertEqual(res.status_code, 405)
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 405)
        self.assertIn('message', data)
        
    def test_405_message_content(self):
        """Verificar mensaje de error 405"""
        res = self.client.delete('/')
        data = json.loads(res.data)
        self.assertIn('Método HTTP no permitido', data['message'])
        
    def test_400_returns_json(self):
        """Verificar que 400 devuelve JSON"""
        res = self.client.post('/api/auth/register', json={
            'username': 'test'
        })
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('message', data)
        
    def test_error_response_has_correct_structure(self):
        """Verificar estructura de respuesta de error"""
        res = self.client.get('/inexistente')
        data = json.loads(res.data)
        self.assertIn('message', data)
        self.assertIn('status_code', data)
        self.assertIn('error', data)
        self.assertEqual(data['status_code'], 404)
        
    def test_cors_headers_on_error_responses(self):
        """Verificar que errores incluyen headers CORS"""
        res = self.client.get('/inexistente', headers={
            'Origin': 'http://localhost:3000'
        })
        self.assertEqual(res.status_code, 404)
        self.assertIn('Access-Control-Allow-Origin', res.headers)
        
    def test_api_404_returns_json(self):
        """Verificar que rutas API inexistentes devuelven JSON"""
        res = self.client.get('/api/auth/inexistente')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 404)
        
    def test_jwt_invalid_returns_json(self):
        """Verificar que token JWT inválido devuelve JSON"""
        res = self.client.get('/protected', headers={
            'Authorization': 'Bearer invalid_token_format'
        })
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertIn('message', data)
        self.assertIn('error', data)

    def test_jwt_expired_returns_401(self):
        """Verificar que token expirado devuelve 401 con mensaje personalizado"""
        from flask_jwt_extended import create_access_token
        from datetime import timedelta
        
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

    def test_422_handler_exists(self):
        """Verificar que el handler 422 está configurado"""
        from werkzeug.exceptions import UnprocessableEntity
        with self.app.test_request_context():
            from flask import current_app
            handler = current_app.error_handler_spec[None].get(422)
            self.assertIsNotNone(handler)

if __name__ == '__main__':
    unittest.main()
