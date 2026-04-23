import unittest
import json
import os

os.environ['FLASK_ENV'] = 'test'

from app import create_app
from app.core.extensions import db
from app.api.roles.models import Roles
from app.api.roles.seeds import seed_roles


class RolesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            seed_roles()
            self.client.post('/api/auth/register', json={
                'username': 'testadmin',
                'email': 'admin@test.com',
                'password': 'password123'
            })
            login_res = self.client.post('/api/auth/login', json={
                'username': 'testadmin',
                'password': 'password123'
            })
            data = json.loads(login_res.data)
            self.access_token = data['data']['access_token']

    def _auth_header(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            try:
                db.drop_all()
            except:
                pass

    def test_get_all_roles(self):
        res = self.client.get('/api/roles')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)

    def test_get_all_roles_returns_seeded_roles(self):
        res = self.client.get('/api/roles')
        data = json.loads(res.data)
        roles = data['data']
        role_names = [r['name'] for r in roles]
        self.assertIn('admin', role_names)
        self.assertIn('agente', role_names)

    def test_get_role_by_id(self):
        res = self.client.get('/api/roles/1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('data', data)
        self.assertEqual(data['data']['id'], 1)

    def test_get_role_by_id_not_found(self):
        res = self.client.get('/api/roles/999')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertIn('Rol no encontrado', data['message'])

    def test_create_role(self):
        res = self.client.post('/api/roles', json={'name': 'gerente'})
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'gerente')
        self.assertTrue(data['data']['status'])

    def test_create_role_missing_name(self):
        res = self.client.post('/api/roles', json={})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('requerido', data['message'])

    def test_create_duplicate_role_name(self):
        self.client.post('/api/roles', json={'name': 'admin'})
        res = self.client.post('/api/roles', json={'name': 'admin'})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('ya existe', data['message'])

    def test_update_role(self):
        res = self.client.put('/api/roles/1', json={'name': 'superadmin'}, headers=self._auth_header())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'superadmin')

    def test_update_role_not_found(self):
        res = self.client.put('/api/roles/999', json={'name': 'test'}, headers=self._auth_header())
        self.assertEqual(res.status_code, 404)

    def test_update_role_duplicate_name(self):
        self.client.post('/api/roles', json={'name': 'gerente'})
        res = self.client.put('/api/roles/1', json={'name': 'gerente'}, headers=self._auth_header())
        self.assertEqual(res.status_code, 400)

    def test_delete_role(self):
        res = self.client.delete('/api/roles/1', headers=self._auth_header())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('eliminado', data['message'])

    def test_delete_role_not_found(self):
        res = self.client.delete('/api/roles/999', headers=self._auth_header())
        self.assertEqual(res.status_code, 404)

    def test_soft_delete_sets_status_false(self):
        self.client.delete('/api/roles/1')
        res = self.client.get('/api/roles/1')
        data = json.loads(res.data)
        self.assertIn('data', data)


if __name__ == '__main__':
    unittest.main()