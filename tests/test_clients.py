import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.clients.models import Client


class ClientsTestCase(unittest.TestCase):
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

    def test_create_client(self):
        res = self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'juan@example.com',
            'phone': '1234567890',
            'address': 'Calle 123',
            'age': 30
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'Juan Perez')
        self.assertEqual(data['data']['email'], 'juan@example.com')

    def test_create_client_duplicate_email(self):
        self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'juan@example.com',
        }, headers=self._auth_headers())

        res = self.client.post('/api/clients', json={
            'name': 'Otro Usuario',
            'email': 'juan@example.com',
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('email', data['message'].lower())

    def test_create_client_invalid_email(self):
        res = self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'not-an-email',
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)

    def test_create_client_missing_name(self):
        res = self.client.post('/api/clients', json={
            'email': 'juan@example.com',
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)

    def test_get_all_clients(self):
        self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'juan@example.com',
        }, headers=self._auth_headers())

        self.client.post('/api/clients', json={
            'name': 'Maria Garcia',
            'email': 'maria@example.com',
        }, headers=self._auth_headers())

        res = self.client.get('/api/clients', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 2)

    def test_get_client_by_id(self):
        create_res = self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'juan@example.com',
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        client_id = created_data['data']['id']

        res = self.client.get(f'/api/clients/{client_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'Juan Perez')

    def test_get_client_not_found(self):
        res = self.client.get('/api/clients/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_update_client(self):
        create_res = self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'juan@example.com',
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        client_id = created_data['data']['id']

        res = self.client.put(f'/api/clients/{client_id}', json={
            'name': 'Juan Actualizado',
            'phone': '9876543210'
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'Juan Actualizado')

    def test_update_client_duplicate_email(self):
        self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'juan@example.com',
        }, headers=self._auth_headers())

        create_res = self.client.post('/api/clients', json={
            'name': 'Maria Garcia',
            'email': 'maria@example.com',
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        client_id = created_data['data']['id']

        res = self.client.put(f'/api/clients/{client_id}', json={
            'email': 'juan@example.com'
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)

    def test_delete_client(self):
        create_res = self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'juan@example.com',
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        client_id = created_data['data']['id']

        res = self.client.delete(f'/api/clients/{client_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)

        get_res = self.client.get(f'/api/clients/{client_id}', headers=self._auth_headers())
        self.assertEqual(get_res.status_code, 404)

    def test_create_client_without_token(self):
        res = self.client.post('/api/clients', json={
            'name': 'Juan Perez',
            'email': 'juan@example.com',
        })
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()