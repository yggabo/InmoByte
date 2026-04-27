import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.filters_properties.models import Property
from app.api.register_and_assign_ownership.models import PropertyStatus
from app.api.agents.models import Agent
from app.api.clients.models import Client

class FiltersPropertiesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Crear registros relacionados
            client = Client(name="Test Client", email="test@example.com")
            status1 = PropertyStatus(id=1, name="DISPONIBLE")
            status2 = PropertyStatus(id=2, name="ASIGNADA")
            status3 = PropertyStatus(id=3, name="VENDIDA")
            db.session.add_all([client, status1, status2, status3])
            db.session.commit()
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
        # Crear algunas propiedades de prueba con el esquema correcto
        prop1 = Property(
            type='house',
            location='Madrid',
            price_min=250000.0,
            price_max=350000.0,
            living_space_min=100.0,
            living_space_max=150.0,
            rooms=3,
            bathrooms=2,
            description='Hermosa casa',
            client_id=1,
            status_id=1  # DISPONIBLE
        )
        prop2 = Property(
            type='apartment',
            location='Barcelona',
            price_min=150000.0,
            price_max=250000.0,
            living_space_min=70.0,
            living_space_max=90.0,
            rooms=2,
            bathrooms=1,
            description='Apartamento moderno',
            client_id=1,
            status_id=1
        )
        prop3 = Property(
            type='land',
            location='Valencia',
            price_min=40000.0,
            price_max=60000.0,
            living_space_min=900.0,
            living_space_max=1100.0,
            rooms=None,
            bathrooms=None,
            description='Terreno amplio',
            client_id=1,
            status_id=3  # VENDIDO
        )
        db.session.add_all([prop1, prop2, prop3])
        db.session.commit()

    def test_get_properties_no_filters(self):
        """Obtener todas las propiedades sin filtros"""
        res = self.client.get('/api/properties')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 3)
        self.assertIn('house', [p['type'] for p in data['data']])

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
        res = self.client.get('/api/properties?min_price=200000&max_price=300000')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        # Debería devolver la casa (price_min=250000, price_max=350000) que se solapa con 200000-300000
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['type'], 'house')

    def test_get_properties_with_multiple_filters(self):
        """Filtrar con múltiples criterios"""
        res = self.client.get('/api/properties?type=apartment&location=Barcelona&min_price=140000')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['type'], 'apartment')

    def test_get_property_by_id_existing(self):
        """Obtener propiedad por ID existente"""
        # Obtener el ID de una propiedad existente
        with self.app.app_context():
            prop = Property.query.filter_by(type='house').first()
            prop_id = prop.id
        
        res = self.client.get(f'/api/properties/{prop_id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['type'], 'house')

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
            'type': 'house',
            'location': 'Sevilla',
            'price_min': 350000.0,
            'price_max': 450000.0,
            'living_space_min': 140.0,
            'living_space_max': 160.0,
            'rooms': 4,
            'bathrooms': 3,
            'description': 'Casa nueva',
            'client_id': 1,
            'status_id': 1
        }
        
        res = self.client.post('/api/properties', 
                             json=new_property_data, 
                             headers=headers)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['type'], 'house')
        self.assertIn('Property created successfully', data['message'])

    def test_create_property_no_auth(self):
        """Intentar crear propiedad sin autenticación"""
        new_property_data = {
            'type': 'house',
            'location': 'Test',
            'price_min': 80000.0,
            'price_max': 120000.0,
            'living_space_min': 100.0,
            'living_space_max': 120.0,
            'rooms': 3,
            'bathrooms': 2,
            'description': 'Casa sin auth',
            'client_id': 1,
            'status_id': 1
        }
        
        res = self.client.post('/api/properties', json=new_property_data)
        self.assertEqual(res.status_code, 401)

    def test_create_property_invalid_data(self):
        """Crear propiedad con datos inválidos"""
        token = self._get_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Datos faltantes - type es requerido
        invalid_data = {'location': 'Casa inválida'}
        
        res = self.client.post('/api/properties', 
                             json=invalid_data, 
                             headers=headers)
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
