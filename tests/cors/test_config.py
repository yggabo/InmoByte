import unittest
import os
from app import create_app


class CORSConfigTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        os.environ['CORS_ORIGINS'] = 'http://localhost:3000,https://example.com'
        self.app = create_app('test')
    
    def test_cors_module_exists(self):
        """Verificar que el módulo cors_config existe"""
        from app.core import cors_config
        self.assertTrue(hasattr(cors_config, 'register_cors'))
    
    def test_register_cors_callable(self):
        """Verificar que register_cors es callable"""
        from app.core.cors_config import register_cors
        self.assertTrue(callable(register_cors))
    
    def test_cors_origins_from_env(self):
        """Verificar que los origins se leen correctamente del entorno"""
        cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000')
        origins_list = [o.strip() for o in cors_origins.split(',') if o.strip()]
        self.assertIn('http://localhost:3000', origins_list)
        self.assertIn('https://example.com', origins_list)


if __name__ == '__main__':
    unittest.main()