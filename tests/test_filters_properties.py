import unittest
import json
import os
from app import create_app
from app.core.extensions import db
from app.api.register_and_assign_ownership.models import Property, PropertyStatus
from app.api.clients.models import Client

class FiltersPropertiesTestCase(unittest.TestCase):
    def setUp(self):
        # Base de datos en memoria para velocidad y limpieza
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_app('test')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Setup base data
            status_1 = PropertyStatus(id=1, name="DISPONIBLE")
            status_2 = PropertyStatus(id=2, name="ASIGNADA")
            client = Client(id=1, name="Juan Vendedor", email="juan@example.com")
            db.session.add_all([status_1, status_2, client])
            
            # Create sample properties
            properties = [
                Property(id=1, type="Casa", location="Valencia", price_min=100000, price_max=120000, 
                         living_space_min=80, living_space_max=100, rooms=3, bathrooms=2, 
                         client_id=1, status_id=1),
                Property(id=2, type="Apartamento", location="Madrid", price_min=150000, price_max=180000, 
                         living_space_min=60, living_space_max=75, rooms=2, bathrooms=1, 
                         client_id=1, status_id=1),
                Property(id=3, type="Casa", location="Madrid", price_min=200000, price_max=250000, 
                         living_space_min=120, living_space_max=150, rooms=4, bathrooms=3, 
                         client_id=1, status_id=2),
                Property(id=4, type="Estudio", location="Barcelona", price_min=80000, price_max=90000, 
                         living_space_min=30, living_space_max=40, rooms=1, bathrooms=1, 
                         client_id=1, status_id=1)
            ]
            db.session.add_all(properties)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _get_token(self):
        self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        login_res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        data = json.loads(login_res.data)
        return data['data']['access_token']

    def test_get_properties_no_filters(self):
        """Test getting all properties when no filters are applied"""
        res = self.client.get('/api/properties/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 4)

    def test_filter_by_type(self):
        """Test filtering by property type"""
        res = self.client.get('/api/properties/?type=Casa')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 2)
        for p in data['data']:
            self.assertEqual(p['type'], "Casa")

    def test_filter_by_location(self):
        """Test filtering by location (case-insensitive and partial match)"""
        res = self.client.get('/api/properties/?location=madrid')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 2)
        for p in data['data']:
            self.assertIn("Madrid", p['location'])

    def test_filter_by_price_range(self):
        """Test filtering by minimum and maximum price"""
        res = self.client.get('/api/properties/?min_price=100000&max_price=160000')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        # Property 1 (100k) and Property 2 (150k) match the price_min criteria
        self.assertEqual(len(data['data']), 2)

    def test_filter_by_rooms_and_bathrooms(self):
        """Test filtering by number of rooms and bathrooms"""
        res = self.client.get('/api/properties/?rooms=3&bathrooms=2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        # Property 1 (3 rooms, 2 baths) and Property 3 (4 rooms, 3 baths) match >= criteria
        self.assertEqual(len(data['data']), 2)

    def test_get_property_detail_success(self):
        """Test getting details of a single property"""
        res = self.client.get('/api/properties/2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['id'], 2)
        self.assertEqual(data['data']['type'], "Apartamento")

    def test_get_property_detail_not_found(self):
        """Test getting details of a non-existent property"""
        res = self.client.get('/api/properties/999')
        self.assertEqual(res.status_code, 404)

    def test_create_property_success(self):
        """Test creating a property with valid data and token"""
        token = self._get_token()
        payload = {
            "type": "Penthouse",
            "location": "Valencia",
            "price_min": 300000,
            "price_max": 350000,
            "living_space_min": 150,
            "living_space_max": 200,
            "rooms": 4,
            "bathrooms": 2,
            "client_id": 1,
            "status_id": 1
        }
        res = self.client.post('/api/properties/', 
                               json=payload, 
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['type'], "Penthouse")
        self.assertEqual(data['message'], "Property created successfully")

    def test_create_property_unauthorized(self):
        """Test creating a property without a token"""
        payload = {"type": "Penthouse"}
        res = self.client.post('/api/properties/', json=payload)
        self.assertEqual(res.status_code, 401)

    def test_create_property_missing_fields(self):
        """Test creating a property with missing required fields"""
        token = self._get_token()
        payload = {"type": "Penthouse"} # Missing many fields
        res = self.client.post('/api/properties/', 
                               json=payload, 
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn("Missing required fields", data['message'])

if __name__ == '__main__':
    unittest.main()
