import unittest
import json
import os
from app import create_app
from app.core.extensions import db
from app.api.filters_properties.models import Property

class FiltersPropertiesTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_app('test')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Crear usuario para JWT
            self.client.post('/api/auth/register', json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            })
            # Crear propiedades de prueba
            self._create_test_properties()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _get_access_token(self):
        login_res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        data = json.loads(login_res.data)
        return data['data']['access_token']

    def _create_test_properties(self):
        # Crear algunas propiedades de prueba
        prop1 = Property(
            title='Casa en Madrid',
            description='Hermosa casa',
            price=300000.0,
            type='house',
            location='Madrid',
            rooms=3,
            bathrooms=2,
            living_space=120.0,
            status_id='available'
        )
        prop2 = Property(
            title='Apartamento en Barcelona',
            description='Apartamento moderno',
            price=200000.0,
            type='apartment',
            location='Barcelona',
            rooms=2,
            bathrooms=1,
            living_space=80.0,
            status_id='available'
        )
        prop3 = Property(
            title='Terreno en Valencia',
            description='Terreno amplio',
            price=50000.0,
            type='land',
            location='Valencia',
            rooms=None,
            bathrooms=None,
            living_space=1000.0,
            status_id='sold'
        )
        db.session.add_all([prop1, prop2, prop3])
        db.session.commit()

    def test_get_properties_no_filters(self):
        """Obtener todas las propiedades sin filtros"""
        res = self.client.get('/api/properties')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 3)
        self.assertIn('Casa en Madrid', [p['title'] for p in data['data']])

    def test_get_properties_with_type_filter(self):
        """Filtrar propiedades por tipo"""
        res = self.client.get('/api/properties?type=house')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['type'], 'house')

    def test_get_properties_with_location_filter(self):
        """Filtrar propiedades por ubicación"""
        res = self.client.get('/api/properties?location=Madrid')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['location'], 'Madrid')

    def test_get_properties_with_price_filters(self):
        """Filtrar propiedades por rango de precio"""
        res = self.client.get('/api/properties?min_price=100000&max_price=250000')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['title'], 'Apartamento en Barcelona')

    def test_get_properties_with_multiple_filters(self):
        """Filtrar con múltiples criterios"""
        res = self.client.get('/api/properties?type=apartment&location=Barcelona&min_price=150000')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['type'], 'apartment')

    def test_get_property_by_id_existing(self):
        """Obtener propiedad por ID existente"""
        # Obtener el ID de una propiedad existente
        with self.app.app_context():
            prop = Property.query.filter_by(title='Casa en Madrid').first()
            prop_id = prop.id
        
        res = self.client.get(f'/api/properties/{prop_id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['title'], 'Casa en Madrid')

    def test_get_property_by_id_not_found(self):
        """Obtener propiedad por ID inexistente"""
        res = self.client.get('/api/properties/999')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertIn('Property not found', data['message'])

    def test_create_property_success(self):
        """Crear una nueva propiedad con autenticación"""
        token = self._get_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        new_property_data = {
            'title': 'Nueva Casa',
            'description': 'Casa nueva',
            'price': 400000.0,
            'type': 'house',
            'location': 'Sevilla',
            'rooms': 4,
            'bathrooms': 3,
            'living_space': 150.0,
            'status_id': 'available'
        }
        
        res = self.client.post('/api/properties', 
                             json=new_property_data, 
                             headers=headers)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['title'], 'Nueva Casa')
        self.assertIn('Property created successfully', data['message'])

    def test_create_property_no_auth(self):
        """Intentar crear propiedad sin autenticación"""
        new_property_data = {
            'title': 'Casa sin auth',
            'price': 100000.0,
            'type': 'house',
            'location': 'Test'
        }
        
        res = self.client.post('/api/properties', json=new_property_data)
        self.assertEqual(res.status_code, 401)

    def test_create_property_invalid_data(self):
        """Crear propiedad con datos inválidos"""
        token = self._get_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Datos faltantes
        invalid_data = {'title': 'Casa inválida'}
        
        res = self.client.post('/api/properties', 
                             json=invalid_data, 
                             headers=headers)
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()</content>
<parameter name="filePath">/home/penascalf5/Escritorio/InmoByte/tests/test_jwt/test_filters_properties.py