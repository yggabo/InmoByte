import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.clients.models import Client
from app.api.propertyStatus.models import PropertyStatus
from app.api.agents.models import Agent
from app.api.userProfile.models import UserProfile
from app.api.roles.models import Roles
from app.api.register_and_assign_ownership.models import Property


class PropertiesTestCase(unittest.TestCase):
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
            # Check if role exists first
            from app.api.roles.models import Roles
            role = Roles.query.filter_by(name='agente').first()
            if not role:
                role = Roles(name='agente', status=True)
                db.session.add(role)
                db.session.flush()

            # Create a test user first
            from app.api.auth.models import Users
            user = Users.query.filter_by(username='testuser_agent').first()
            if not user:
                from werkzeug.security import generate_password_hash
                user = Users(
                    username='testuser_agent',
                    email='agent@example.com',
                    password_hash=generate_password_hash('password123')
                )
                db.session.add(user)
                db.session.flush()

            # Create user profile for agent
            user_profile = UserProfile(
                name='Agent',
                lastNames='Test',
                telefono='123456789',
                rolId=role.id,
                userId=user.id
            )
            db.session.add(user_profile)
            db.session.flush()

            # Create agent
            agent = Agent(userProfileId=user_profile.id, status=True)
            db.session.add(agent)

            # Check if property status exists
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

            db.session.commit()

            # Store IDs for use in tests
            self.agent_id = agent.id
            self.status_id = status.id
            self.client_id = client.id

    def test_create_property(self):
        res = self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Casa',
            'location': 'Madrid',
            'price_min': 100000,
            'price_max': 150000,
            'living_space': 100,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': self.client_id,
            'status_id': self.status_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['type'], 'Casa')
        self.assertEqual(data['location'], 'Madrid')

    def test_create_property_invalid_data(self):
        res = self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Ca',
            'location': 'Madrid',
            'price_min': 150000,
            'price_max': 100000,
            'living_space': 100,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': self.client_id,
            'status_id': self.status_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('error', data)

    def test_create_property_missing_fields(self):
        res = self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Casa'
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 400)

    def test_get_all_properties(self):
        self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Casa',
            'location': 'Madrid',
            'price_min': 100000,
            'price_max': 150000,
            'living_space': 100,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': self.client_id,
            'status_id': self.status_id
        }, headers=self._auth_headers())

        res = self.client.get('/api/register-and-assign-ownership/properties', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data), 1)

    def test_get_property_by_id(self):
        create_res = self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Casa',
            'location': 'Madrid',
            'price_min': 100000,
            'price_max': 150000,
            'living_space': 100,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': self.client_id,
            'status_id': self.status_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        property_id = created_data['id']

        res = self.client.get(f'/api/register-and-assign-ownership/properties/{property_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['id'], property_id)

    def test_get_property_not_found(self):
        res = self.client.get('/api/register-and-assign-ownership/properties/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_update_property(self):
        create_res = self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Casa',
            'location': 'Madrid',
            'price_min': 100000,
            'price_max': 150000,
            'living_space': 100,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': self.client_id,
            'status_id': self.status_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        property_id = created_data['id']

        res = self.client.put(f'/api/register-and-assign-ownership/properties/{property_id}', json={
            'location': 'Barcelona',
            'price_max': 200000
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['location'], 'Barcelona')
        self.assertEqual(float(data['price_max']), 200000)

    def test_update_property_not_found(self):
        res = self.client.put('/api/register-and-assign-ownership/properties/9999', json={
            'location': 'Barcelona'
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 404)

    def test_delete_property(self):
        create_res = self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Casa',
            'location': 'Madrid',
            'price_min': 100000,
            'price_max': 150000,
            'living_space': 100,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': self.client_id,
            'status_id': self.status_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        property_id = created_data['id']

        res = self.client.delete(f'/api/register-and-assign-ownership/properties/{property_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)

        get_res = self.client.get(f'/api/register-and-assign-ownership/properties/{property_id}', headers=self._auth_headers())
        self.assertEqual(get_res.status_code, 404)

    def test_delete_property_not_found(self):
        res = self.client.delete('/api/register-and-assign-ownership/properties/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_assign_agent(self):
        create_res = self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Casa',
            'location': 'Madrid',
            'price_min': 100000,
            'price_max': 150000,
            'living_space': 100,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': self.client_id,
            'status_id': self.status_id
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        property_id = created_data['id']

        res = self.client.patch(f'/api/register-and-assign-ownership/properties/{property_id}/assign-agent', json={
            'agent_id': self.agent_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['agent']['id'], self.agent_id)

    def test_assign_agent_property_not_found(self):
        res = self.client.patch('/api/register-and-assign-ownership/properties/9999/assign-agent', json={
            'agent_id': self.agent_id
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 404)

    def test_create_property_without_token(self):
        res = self.client.post('/api/register-and-assign-ownership/properties', json={
            'type': 'Casa',
            'location': 'Madrid',
            'price_min': 100000,
            'price_max': 150000,
            'living_space': 100,
            'rooms': 3,
            'bathrooms': 2,
            'client_id': self.client_id,
            'status_id': self.status_id
        })

        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
