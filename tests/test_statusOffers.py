import unittest
import json
from app import create_app
from app.core.extensions import db
from app.api.statusOffers.models import OfferStatus
from app.api.auth.models import Users as User


class OfferStatusTestCase(unittest.TestCase):
    """Test cases for OfferStatus endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        # Import models before creating app to ensure they're registered
        from app.api.statusOffers.models import OfferStatus
        from app.api.auth.models import Users as User
        
        self.app = create_app('test')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Seed OfferStatus records
        self._seed_offer_statuses()
        
        # Register and login a user to get JWT token
        self._register_and_login()
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def _seed_offer_statuses(self):
        """Seed OfferStatus records for testing."""
        statuses = [
            {'name': 'Pending', 'status': True},
            {'name': 'Accepted', 'status': True},
            {'name': 'Rejected', 'status': True},
            {'name': 'Cancelled', 'status': True},
        ]
        for status_data in statuses:
            # Check if already exists
            existing = OfferStatus.query.filter_by(name=status_data['name']).first()
            if not existing:
                status = OfferStatus(
                    name=status_data['name'],
                    status=status_data['status']
                )
                db.session.add(status)
        db.session.commit()
    
    def _register_and_login(self):
        """Register a test user and login to get JWT token."""
        # Register user
        register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test1234'
        }
        self.client.post('/api/auth/register', json=register_data)
        
        # Login to get token
        login_data = {
            'username': 'testuser',
            'password': 'Test1234'
        }
        login_res = self.client.post('/api/auth/login', json=login_data)
        login_json = json.loads(login_res.data)
        self.access_token = login_json['data']['access_token']
    
    def _auth_headers(self):
        """Return headers with JWT token."""
        return {'Authorization': f'Bearer {self.access_token}'}
    
    def test_get_all_offer_statuses(self):
        """Test GET /api/status-offers - Get all offer statuses."""
        res = self.client.get('/api/status-offers', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('data', data)
        self.assertGreater(len(data['data']), 0)
    
    def test_get_offer_status_by_id(self):
        """Test GET /api/status-offers/<id> - Get offer status by ID."""
        # Get first status
        status = OfferStatus.query.first()
        res = self.client.get(f'/api/status-offers/{status.id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['id'], status.id)
        self.assertEqual(data['data']['name'], status.name)
    
    def test_get_offer_status_not_found(self):
        """Test GET /api/status-offers/<id> with non-existent ID."""
        res = self.client.get('/api/status-offers/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)
    
    def test_create_offer_status(self):
        """Test POST /api/status-offers - Create new offer status."""
        res = self.client.post('/api/status-offers', json={
            'name': 'Under Review',
            'status': True
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'Under Review')
    
    def test_create_offer_status_duplicate_name(self):
        """Test POST /api/status-offers with duplicate name."""
        res = self.client.post('/api/status-offers', json={
            'name': 'Pending',
            'status': True
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 400)
    
    def test_update_offer_status(self):
        """Test PUT /api/status-offers/<id> - Update offer status."""
        status = OfferStatus.query.filter_by(name='Pending').first()
        res = self.client.put(f'/api/status-offers/{status.id}', json={
            'name': 'On Hold',
            'status': False
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['data']['name'], 'On Hold')
    
    def test_update_offer_status_not_found(self):
        """Test PUT /api/status-offers/<id> with non-existent ID."""
        res = self.client.put('/api/status-offers/9999', json={
            'name': 'New Name'
        }, headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)
    
    def test_delete_offer_status(self):
        """Test DELETE /api/status-offers/<id> - Soft delete offer status."""
        # Create a status to delete
        status = OfferStatus(name='To Delete', status=True)
        db.session.add(status)
        db.session.commit()
        status_id = status.id
        
        res = self.client.delete(f'/api/status-offers/{status_id}', headers=self._auth_headers())
        self.assertEqual(res.status_code, 200)
        
        # Verify it's soft-deleted (status set to False)
        deleted = db.session.get(OfferStatus, status_id)
        self.assertIsNotNone(deleted)
        self.assertFalse(deleted.status)
    
    def test_delete_offer_status_not_found(self):
        """Test DELETE /api/status-offers/<id> with non-existent ID."""
        res = self.client.delete('/api/status-offers/9999', headers=self._auth_headers())
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
