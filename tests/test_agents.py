import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.agents.models import Agent
from app.api.userProfile.models import UserProfile
from app.api.roles.models import Roles
from app.api.auth.models import Users


class AgentsTestCase(unittest.TestCase):
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

    def _create_user_profile(self, userId, rolId=1):
        from app.core.extensions import bcrypt
        with self.app.app_context():
            user = Users(
                id=userId,
                username=f'user{userId}',
                email=f'user{userId}@test.com',
                password_hash=bcrypt.generate_password_hash('password123').decode('utf-8')
            )
            db.session.add(user)
            
            rol = Roles.query.filter(Roles.id == rolId).first()
            if not rol:
                rol = Roles(id=rolId, name='agente', status=True)
                db.session.add(rol)
            
            profile = UserProfile(
                id=userId,
                name=f'User',
                lastNames=f'Test{userId}',
                telefono='1234567890',
                rolId=rolId,
                userId=userId
            )
            db.session.add(profile)
            db.session.commit()
            return profile

    def test_create_agent(self):
        self._create_user_profile(2)
        
        res = self.client.post('/api/agents', json={
            'userProfileId': 2
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['userProfileId'], 2)
        self.assertEqual(data['data']['status'], True)

    def test_create_duplicate_agent(self):
        self._create_user_profile(2)
        
        self.client.post('/api/agents', json={
            'userProfileId': 2
        }, headers=self._auth_headers())
        
        res = self.client.post('/api/agents', json={
            'userProfileId': 2
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('ya existe', data['message'].lower())

    def test_get_all_agents(self):
        self._create_user_profile(2)
        self.client.post('/api/agents', json={
            'userProfileId': 2
        }, headers=self._auth_headers())

        res = self.client.get('/api/agents', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 1)

    def test_get_agent_by_id(self):
        self._create_user_profile(2)
        
        create_res = self.client.post('/api/agents', json={
            'userProfileId': 2
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        agent_id = created_data['data']['id']

        res = self.client.get(f'/api/agents/{agent_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['userProfileId'], 2)

    def test_get_agent_not_found(self):
        res = self.client.get('/api/agents/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_delete_agent(self):
        self._create_user_profile(2)
        
        create_res = self.client.post('/api/agents', json={
            'userProfileId': 2
        }, headers=self._auth_headers())
        created_data = json.loads(create_res.data)
        agent_id = created_data['data']['id']

        res = self.client.delete(f'/api/agents/{agent_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)

        get_res = self.client.get(f'/api/agents/{agent_id}', headers=self._auth_headers())
        data = json.loads(get_res.data)
        self.assertEqual(data['data']['status'], False)

    def test_delete_agent_not_found(self):
        res = self.client.delete('/api/agents/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)

    def test_create_agent_without_token(self):
        res = self.client.post('/api/agents', json={
            'userProfileId': 1
        })
        self.assertEqual(res.status_code, 401)

    def test_get_agents_filter_by_status(self):
        self._create_user_profile(2)
        
        self.client.post('/api/agents', json={
            'userProfileId': 2
        }, headers=self._auth_headers())

        res = self.client.get('/api/agents?status=true', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['data']), 1)


if __name__ == '__main__':
    unittest.main()