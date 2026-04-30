import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.clients.models import Client
from app.api.propertyStatus.models import PropertyStatus
from app.api.register_and_assign_ownership.models import Property


class FiltersPropertiesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self._seed_test_data()

        self._register_and_login()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _register_and_login(self):
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
        self.access_token = data['data']['access_token']

    def _auth_headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def _seed_test_data(self):
        with self.app.app_context():
            # Check if property status exists
            from app.api.propertyStatus.models import PropertyStatus
            status = PropertyStatus.query.filter_by(name='en venta').first()
            if not status:
                status = PropertyStatus(name='en venta', status=True, accepts_offers=True)
                db.session.add(status)
                db.session.flush()

            # Check if client exists
            client = Client.query.filter_by(email='john@example.com').first()
            if not client:
                client = Client(name='John', email='john@example.com', phone='1234567890', address='123 Main St', age=30)
                db.session.add(client)
                db.session.flush()

            # Create multiple properties for testing filters
            properties = [
                Property(
                    type='Casa',
                    location='Madrid',
                    price_min=100000,
                    price_max=150000,
                    living_space=100,
                    rooms=3,
                    bathrooms=2,
                    description='House in Madrid',
                    client_id=client.id,
                    status_id=status.id
                ),
                Property(
                    type='Apartamento',
                    location='Barcelona',
                    price_min=80000,
                    price_max=120000,
                    living_space=80,
                    rooms=2,
                    bathrooms=1,
                    description='Apartment in Barcelona',
                    client_id=client.id,
                    status_id=status.id
                ),
                Property(
                    type='Casa',
                    location='Madrid',
                    price_min=200000,
                    price_max=250000,
                    living_space=150,
                    rooms=4,
                    bathrooms=3,
                    description='Big house in Madrid',
                    client_id=client.id,
                    status_id=status.id
                )
            ]
            db.session.add_all(properties)
            db.session.commit()

    def test_search_no_filters(self):
        res = self.client.get('/api/filter-properties/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 3)

    def test_search_by_type(self):
        res = self.client.get('/api/filter-properties/?type=Casa')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['type'], 'Casa')

    def test_search_by_location(self):
        res = self.client.get('/api/filter-properties/?location=Madrid')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['location'], 'Madrid')

    def test_search_by_price_range(self):
        res = self.client.get('/api/filter-properties/?price_min=90000&price_max=160000')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 1)

    def test_search_by_rooms(self):
        res = self.client.get('/api/filter-properties/?rooms=3')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['rooms'], 3)

    def test_search_by_bathrooms(self):
        res = self.client.get('/api/filter-properties/?bathrooms=2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['bathrooms'], 2)

    def test_search_combined_filters(self):
        res = self.client.get('/api/filter-properties/?type=Casa&location=Madrid&rooms=3')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['type'], 'Casa')
            self.assertEqual(prop['location'], 'Madrid')
            self.assertEqual(prop['rooms'], 3)

    def test_search_no_results(self):
        res = self.client.get('/api/filter-properties/?location=NonExistentCity')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 0)

    def test_get_property_by_id(self):
        res = self.client.get('/api/filter-properties/1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['id'], 1)

    def test_get_property_not_found(self):
        res = self.client.get('/api/filter-properties/9999')
        self.assertEqual(res.status_code, 404)

    def test_create_property(self):
        res = self.client.post('/api/filter-properties/', json={
            'type': 'Casa',
            'location': 'Valencia',
            'price_min': 150000,
            'price_max': 200000,
            'living_space': 90,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': 1,
            'status_id': 1
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['location'], 'Valencia')

    def test_search_no_filters(self):
        res = self.client.get('/api/filter-properties/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 3)

    def test_search_by_type(self):
        res = self.client.get('/api/filter-properties/?type=Casa')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['type'], 'Casa')

    def test_search_by_location(self):
        res = self.client.get('/api/filter-properties/?location=Madrid')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['location'], 'Madrid')

    def test_search_by_price_range(self):
        res = self.client.get('/api/filter-properties/?price_min=90000&price_max=160000')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 1)

    def test_search_by_rooms(self):
        res = self.client.get('/api/filter-properties/?rooms=3')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['rooms'], 3)

    def test_search_by_bathrooms(self):
        res = self.client.get('/api/filter-properties/?bathrooms=2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['bathrooms'], 2)

    def test_search_combined_filters(self):
        res = self.client.get('/api/filter-properties/?type=Casa&location=Madrid&rooms=3')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for prop in data['data']:
            self.assertEqual(prop['type'], 'Casa')
            self.assertEqual(prop['location'], 'Madrid')
            self.assertEqual(prop['rooms'], 3)

    def test_search_no_results(self):
        res = self.client.get('/api/filter-properties/?location=NonExistentCity')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 0)

    def test_get_property_by_id(self):
        res = self.client.get('/api/filter-properties/1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['id'], 1)

    def test_get_property_not_found(self):
        res = self.client.get('/api/filter-properties/9999')
        self.assertEqual(res.status_code, 404)

    def test_create_property(self):
        res = self.client.post('/api/filter-properties/', json={
            'type': 'Casa',
            'location': 'Valencia',
            'price_min': 150000,
            'price_max': 200000,
            'living_space': 90,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': 1,
            'status_id': 1
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['location'], 'Valencia')

    def test_create_property_missing_fields(self):
        res = self.client.post('/api/filter-properties/', json={
            'type': 'Casa'
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('Missing', data['message'])

    def test_create_property_without_token(self):
        res = self.client.post('/api/filter-properties/', json={
            'type': 'Casa',
            'location': 'Valencia',
            'price_min': 150000,
            'price_max': 200000,
            'living_space_min': 90,
            'living_space_max': 110,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': 1,
            'status_id': 1
        })

        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
