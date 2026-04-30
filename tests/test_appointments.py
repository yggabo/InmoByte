import unittest
import json
from datetime import date, time
from app import create_app
from app.core.extensions import db
from app.api.clients.models import Client
from app.api.register_and_assign_ownership.models import Property
from app.api.agents.models import Agent
from app.api.userProfile.models import UserProfile
from app.api.roles.models import Roles
from app.api.auth.models import Users
from app.api.appointments_scheduling.models import Appointment, AppointmentStatus
from app.api.propertyStatus.models import PropertyStatus


class AppointmentsTestCase(unittest.TestCase):
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
            # Create Role
            role = Roles.query.filter_by(name='agente').first()
            if not role:
                role = Roles(name='agente', status=True)
                db.session.add(role)
                db.session.flush()

            # Create User for Agent
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

            # Create UserProfile
            user_profile = UserProfile.query.filter_by(userId=user.id).first()
            if not user_profile:
                user_profile = UserProfile(
                    name='Agent',
                    lastNames='Test',
                    telefono='123456789',
                    rolId=role.id,
                    userId=user.id
                )
                db.session.add(user_profile)
                db.session.flush()

            # Create Agent
            agent = Agent.query.filter_by(userProfileId=user_profile.id).first()
            if not agent:
                agent = Agent(userProfileId=user_profile.id, status=True)
                db.session.add(agent)
                db.session.flush()

            # Create PropertyStatus
            prop_status = PropertyStatus.query.filter_by(name='en venta').first()
            if not prop_status:
                prop_status = PropertyStatus(name='en venta', status=True, accepts_offers=True)
                db.session.add(prop_status)
                db.session.flush()

            # Create Client
            client = Client.query.filter_by(email='john@example.com').first()
            if not client:
                client = Client(name='John', email='john@example.com', phone='1234567890', address='123 Main St', age=30)
                db.session.add(client)
                db.session.flush()

            # Create Property with agent assigned
            property_obj = Property.query.filter_by(location='Madrid').first()
            if not property_obj:
                property_obj = Property(
                    type='Casa',
                    location='Madrid',
                    price_min=100000,
                    price_max=150000,
                    living_space=100,
                    rooms=3,
                    bathrooms=2,
                    description='Test house',
                    client_id=client.id,
                    status_id=prop_status.id,
                    agent_id=agent.id
                )
                db.session.add(property_obj)
                db.session.flush()

            # Create AppointmentStatus
            status_prog = AppointmentStatus.query.filter_by(name='PROGRAMADA').first()
            if not status_prog:
                status_prog = AppointmentStatus(name='PROGRAMADA', description='Cita programada', status=True)
                db.session.add(status_prog)

            status_real = AppointmentStatus.query.filter_by(name='REALIZADA').first()
            if not status_real:
                status_real = AppointmentStatus(name='REALIZADA', description='Cita realizada', status=True)
                db.session.add(status_real)

            status_canc = AppointmentStatus.query.filter_by(name='CANCELADA').first()
            if not status_canc:
                status_canc = AppointmentStatus(name='CANCELADA', description='Cita cancelada', status=True)
                db.session.add(status_canc)

            db.session.commit()

            # Store IDs
            self.agent_id = agent.id
            self.client_id = client.id
            self.property_id = property_obj.id
            self.status_prog_id = status_prog.id if status_prog else 1
            self.status_real_id = status_real.id if status_real else 2

    # ==================== CREATE TESTS ====================

    def test_create_appointment(self):
        res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
            'notes': 'Cita de prueba'
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['appointment_date'], '2026-05-15')
        self.assertEqual(data['data']['client_name'], 'John')
        self.assertEqual(data['data']['property_location'], 'Madrid')

    def test_create_appointment_without_token(self):
        res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
        })
        self.assertEqual(res.status_code, 401)

    def test_create_appointment_missing_fields(self):
        res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15'
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)

    def test_create_appointment_invalid_date(self):
        res = self.client.post('/api/appointments', json={
            'appointment_date': 'invalid-date',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)

    def test_create_appointment_invalid_time(self):
        res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': 'invalid-time',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)

    def test_create_appointment_conflict(self):
        # Create first appointment
        self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        # Try to create overlapping appointment
        res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:30:00',  # Overlaps
            'end_time': '11:30:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 409)

    def test_create_appointment_auto_assign_agent(self):
        # Don't provide agent_id, should use property's agent
        res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '14:00:00',
            'end_time': '15:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            # No agent_id - should use property's agent
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['agent_id'], self.agent_id)

    # ==================== LIST TESTS ====================

    def test_get_all_appointments(self):
        # Create an appointment first
        self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        res = self.client.get('/api/appointments', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 1)

    def test_get_appointments_by_date(self):
        self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        res = self.client.get('/api/appointments?date=2026-05-15', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 1)
        for apt in data['data']:
            self.assertEqual(apt['appointment_date'], '2026-05-15')

    def test_get_appointments_by_client(self):
        self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        res = self.client.get(f'/api/appointments?client_id={self.client_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 1)
        for apt in data['data']:
            self.assertEqual(apt['client_id'], self.client_id)

    def test_get_appointments_by_agent(self):
        self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        res = self.client.get(f'/api/appointments?agent_id={self.agent_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 1)
        for apt in data['data']:
            self.assertEqual(apt['agent_id'], self.agent_id)

    def test_get_appointments_by_property(self):
        self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        res = self.client.get(f'/api/appointments?property_id={self.property_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['data']), 1)
        for apt in data['data']:
            self.assertEqual(apt['property_id'], self.property_id)

    # ==================== UPDATE TESTS ====================

    def test_update_appointment(self):
        create_res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        appointment_id = created_data['data']['id']

        res = self.client.put(f'/api/appointments/{appointment_id}', json={
            'notes': 'Notas actualizadas'
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['notes'], 'Notas actualizadas')

    def test_update_appointment_not_found(self):
        res = self.client.put('/api/appointments/9999', json={
            'notes': 'Updated'
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_update_appointment_without_token(self):
        res = self.client.put('/api/appointments/1', json={
            'notes': 'Updated'
        })
        self.assertEqual(res.status_code, 401)

    def test_update_appointment_conflict(self):
        # Create first appointment
        self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        # Create second appointment
        create_res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '12:00:00',
            'end_time': '13:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        appointment_id = created_data['data']['id']

        # Try to update second appointment to overlap with first
        res = self.client.put(f'/api/appointments/{appointment_id}', json={
            'start_time': '10:30:00',
            'end_time': '11:30:00',
        }, headers=self._auth_headers())

        self.assertEqual(res.status_code, 409)

    # ==================== DELETE TESTS ====================

    def test_delete_appointment(self):
        create_res = self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        appointment_id = created_data['data']['id']

        res = self.client.delete(f'/api/appointments/{appointment_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)

        # Verify soft delete - should return 404 now
        get_res = self.client.get(f'/api/appointments?date=2026-05-15', headers=self._auth_headers())
        data = json.loads(get_res.data)
        for apt in data['data']:
            self.assertNotEqual(apt['id'], appointment_id)

    def test_delete_appointment_not_found(self):
        res = self.client.delete('/api/appointments/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_delete_appointment_without_token(self):
        res = self.client.delete('/api/appointments/1')
        self.assertEqual(res.status_code, 401)

    # ==================== PROPERTY APPOINTMENTS TESTS ====================

    def test_get_property_appointments(self):
        # Create an appointment
        self.client.post('/api/appointments', json={
            'appointment_date': '2026-05-15',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'client_id': self.client_id,
            'property_id': self.property_id,
            'agent_id': self.agent_id,
        }, headers=self._auth_headers())

        res = self.client.get(f'/api/register-and-assign-ownership/properties/{self.property_id}/appointments', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data), 1)

    def test_get_property_appointments_not_found(self):
        res = self.client.get('/api/register-and-assign-ownership/properties/9999/appointments', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
