import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.propertyStatus.models import PropertyStatus


class PropertyStatusTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self._register_and_login()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _register_and_login(self):
        # Registrar usuario y obtener token JWT
        self.client.post('/api/auth/register', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test1234"
        })
        login_res = self.client.post('/api/auth/login', json={
            "username": "testuser",
            "password": "Test1234"
        })
        data = json.loads(login_res.data)
        self.access_token = data['data']['access_token']

    def _auth_headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def test_create_property_status(self):
        res = self.client.post('/api/property-status',
                              json={'name': 'en venta'},
                              headers=self._auth_headers())
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'en venta')

    def test_get_all_property_statuses(self):
        # Sembrar datos primero
        with self.app.app_context():
            db.session.add(PropertyStatus(name="test status", status=True))
            db.session.commit()
        res = self.client.get('/api/property-status', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreater(len(data['data']), 0)

    def test_get_property_status_by_id(self):
        with self.app.app_context():
            ps = PropertyStatus(name="test status 2", status=True)
            db.session.add(ps)
            db.session.commit()
            ps_id = ps.id
        res = self.client.get(f'/api/property-status/{ps_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'test status 2')

    def test_update_property_status(self):
        with self.app.app_context():
            ps = PropertyStatus(name="old name", status=True)
            db.session.add(ps)
            db.session.commit()
            ps_id = ps.id
        res = self.client.put(f'/api/property-status/{ps_id}',
                             json={'name': 'new name'},
                             headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'new name')

    def test_delete_property_status(self):
        with self.app.app_context():
            ps = PropertyStatus(name="to delete", status=True)
            db.session.add(ps)
            db.session.commit()
            ps_id = ps.id
        res = self.client.delete(f'/api/property-status/{ps_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        # Verificar que se hizo soft delete
        with self.app.app_context():
            ps = db.session.get(PropertyStatus, ps_id)
            self.assertFalse(ps.status)

    def test_create_duplicate_property_status(self):
        self.client.post('/api/property-status',
                        json={'name': 'duplicate'},
                        headers=self._auth_headers())
        res = self.client.post('/api/property-status',
                              json={'name': 'duplicate'},
                              headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
