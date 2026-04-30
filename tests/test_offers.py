import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.clients.models import Client
from app.api.propertyStatus.models import PropertyStatus
from app.api.offers.models import Offer
from app.api.statusOffers.models import OfferStatus
from app.api.register_and_assign_ownership.models import Property


class OffersTestCase(unittest.TestCase):
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
            # Create offer status
            from app.api.statusOffers.models import OfferStatus
            status1 = OfferStatus.query.filter_by(name='Pendiente').first()
            if not status1:
                status1 = OfferStatus(name='Pendiente')
                db.session.add(status1)
            
            status2 = OfferStatus.query.filter_by(name='Aceptada').first()
            if not status2:
                status2 = OfferStatus(name='Aceptada')
                db.session.add(status2)
            
            status3 = OfferStatus.query.filter_by(name='Rechazada').first()
            if not status3:
                status3 = OfferStatus(name='Rechazada')
                db.session.add(status3)
            
            status4 = OfferStatus.query.filter_by(name='Cancelada').first()
            if not status4:
                status4 = OfferStatus(name='Cancelada')
                db.session.add(status4)
            
            db.session.flush()

            # Create property status (accepts_offers=True)
            from app.api.propertyStatus.models import PropertyStatus
            prop_status = PropertyStatus.query.filter_by(name='en venta').first()
            if not prop_status:
                prop_status = PropertyStatus(name='en venta', status=True, accepts_offers=True)
                db.session.add(prop_status)
                db.session.flush()

            # Create client
            from app.api.clients.models import Client
            client = Client.query.filter_by(email='john@example.com').first()
            if not client:
                client = Client(name='John', email='john@example.com', phone='1234567890', address='123 Main St', age=30)
                db.session.add(client)
                db.session.flush()

            # Create property
            from app.api.register_and_assign_ownership.models import Property
            property = Property.query.filter_by(location='Madrid').first()
            if not property:
                property = Property(
                    type='Casa',
                    location='Madrid',
                    price_min=100000,
                    price_max=150000,
                    living_space=100,
                    rooms=3,
                    bathrooms=2,
                    description='Nice house',
                    client_id=client.id,
                    status_id=prop_status.id
                )
                db.session.add(property)
            
            db.session.commit()

            # Store IDs
            self.client_id = client.id
            self.property_id = property.id
            self.pending_status_id = status1.id if status1 else 1
            self.accepted_status_id = status2.id if status2 else 2
            self.rejected_status_id = status3.id if status3 else 3
            self.cancelled_status_id = status4.id if status4 else 4

    def test_create_offer(self):
        res = self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(float(data['offered_price']), 120000)
        self.assertEqual(data['status'], 'Pendiente')

    def test_create_offer_invalid_data(self):
        res = self.client.post('/api/offers/', json={
            'offered_price': -1000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 400)

    def test_create_offer_missing_fields(self):
        res = self.client.post('/api/offers/', json={
            'offered_price': 120000
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 400)

    def test_create_offer_property_not_accepting_offers(self):
        with self.app.app_context():
            from app.api.propertyStatus.models import PropertyStatus
            from app.api.register_and_assign_ownership.models import Property
            from app.api.clients.models import Client
            
            # Create property status that doesn't accept offers
            prop_status = PropertyStatus.query.filter_by(name='vendido').first()
            if not prop_status:
                prop_status = PropertyStatus(name='vendido', status=True, accepts_offers=False)
                db.session.add(prop_status)
                db.session.flush()
            
            # Create property with accepts_offers=False
            client_obj = Client.query.filter_by(email='john@example.com').first()
            property = Property(
                type='Apartamento',
                location='Barcelona',
                price_min=200000,
                price_max=250000,
                living_space=80,
                rooms=2,
                bathrooms=1,
                description='Nice apartment',
                client_id=client_obj.id,
                status_id=prop_status.id
            )
            db.session.add(property)
            db.session.commit()
            sold_property_id = property.id

        res = self.client.post('/api/offers/', json={
            'offered_price': 220000,
            'property_id': sold_property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 409)

    def test_get_all_offers(self):
        self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())

        res = self.client.get('/api/offers', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data), 1)

    def test_get_offers_with_property_filter(self):
        self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())

        res = self.client.get(f'/api/offers?property_id={self.property_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for offer in data:
            self.assertEqual(offer['property_id'], self.property_id)

    def test_get_offers_with_client_filter(self):
        self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())

        res = self.client.get(f'/api/offers?client_id={self.client_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        for offer in data:
            self.assertEqual(offer['client_id'], self.client_id)

    def test_get_offer_by_id(self):
        create_res = self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        offer_id = created_data['id']

        res = self.client.get(f'/api/offers/{offer_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['id'], offer_id)

    def test_get_offer_not_found(self):
        res = self.client.get('/api/offers/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_get_property_offers(self):
        self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())

        res = self.client.get(f'/api/offers/properties/{self.property_id}/offers', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data), 1)

    def test_get_property_offers_not_found(self):
        res = self.client.get('/api/offers/properties/9999/offers', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_update_offer_status_accept(self):
        create_res = self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        offer_id = created_data['data']['id']

        res = self.client.patch(f'/api/offers/{offer_id}/status', json={
            'status_id': self.accepted_status_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['status'], 'Aceptada')

    def test_update_offer_status_reject(self):
        create_res = self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        offer_id = created_data['id']

        res = self.client.patch(f'/api/offers/{offer_id}/status', json={
            'status_id': self.rejected_status_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'Rechazada')

    def test_update_offer_status_cancel(self):
        create_res = self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        offer_id = created_data['id']

        res = self.client.patch(f'/api/offers/{offer_id}/status', json={
            'status_id': self.cancelled_status_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'Cancelada')

    def test_update_offer_status_invalid_id(self):
        create_res = self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        offer_id = created_data['id']

        res = self.client.patch(f'/api/offers/{offer_id}/status', json={
            'status_id': 999
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 400)

    def test_update_offer_status_not_found(self):
        res = self.client.patch('/api/offers/9999/status', json={
            'status_id': self.accepted_status_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 404)

    def test_create_offer_without_token(self):
        res = self.client.post('/api/offers/', json={
            'offered_price': 120000,
            'property_id': self.property_id,
            'client_id': self.client_id
        })

        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
