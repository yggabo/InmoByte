import pytest
import json
import os
from app import create_app
from app.core.extensions import db as _db
from app.api.statusOffers.models import OfferStatus
from app.api.auth.models import Users as User

@pytest.fixture(scope='module')
def app():
    """Configuración de la aplicación para pruebas."""
    if not os.environ.get('SQLALCHEMY_DATABASE_URI'):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_TEST_NAME', 'app_db_test')}"
        )
    
    _app = create_app('test')
    return _app

@pytest.fixture
def client(app):
    """Cliente de pruebas de Flask."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Base de datos limpia para cada test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def jwt_headers(client, db):
    """Registra usuario y genera headers con JWT token."""
    # Registro de usuario (asumiendo que auth/register está disponible)
    client.post('/api/auth/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test1234"
    })
    login_res = client.post('/api/auth/login', json={
        "username": "testuser",
        "password": "Test1234"
    })
    data = json.loads(login_res.data)
    access_token = data['data']['access_token']
    return {'Authorization': f'Bearer {access_token}'}

def test_create_offer_status(client, db, jwt_headers):
    res = client.post('/api/status-offers',
                       json={'name': 'Pendiente'},
                       headers=jwt_headers)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['data']['name'] == 'Pendiente'

def test_get_all_offer_statuses(client, db, jwt_headers):
    # Sembrar datos primero
    with client.application.app_context():
        db.session.add(OfferStatus(name="Test Status", status=True))
        db.session.commit()
    res = client.get('/api/status-offers', headers=jwt_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data['data']) > 0

def test_get_offer_status_by_id(client, db, jwt_headers):
    with client.application.app_context():
        os = OfferStatus(name="Test Status 2", status=True)
        db.session.add(os)
        db.session.commit()
        os_id = os.id
    res = client.get(f'/api/status-offers/{os_id}', headers=jwt_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['data']['name'] == 'Test Status 2'

def test_update_offer_status(client, db, jwt_headers):
    with client.application.app_context():
        os = OfferStatus(name="Old Name", status=True)
        db.session.add(os)
        db.session.commit()
        os_id = os.id
    res = client.put(f'/api/status-offers/{os_id}',
                      json={'name': 'New Name'},
                      headers=jwt_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['data']['name'] == 'New Name'

def test_delete_offer_status(client, db, jwt_headers):
    with client.application.app_context():
        os = OfferStatus(name="To Delete", status=True)
        db.session.add(os)
        db.session.commit()
        os_id = os.id
    res = client.delete(f'/api/status-offers/{os_id}', headers=jwt_headers)
    assert res.status_code == 200
    # Verificar que se hizo soft delete
    with client.application.app_context():
        os = db.session.get(OfferStatus, os_id)
        assert os.status == False

def test_create_duplicate_offer_status(client, db, jwt_headers):
    client.post('/api/status-offers',
                 json={'name': 'Duplicate'},
                 headers=jwt_headers)
    res = client.post('/api/status-offers',
                      json={'name': 'Duplicate'},
                      headers=jwt_headers)
    assert res.status_code == 400

def test_get_nonexistent_offer_status(client, jwt_headers):
    res = client.get('/api/status-offers/9999', headers=jwt_headers)
    assert res.status_code == 404

def test_update_nonexistent_offer_status(client, jwt_headers):
    res = client.put('/api/status-offers/9999',
                     json={'name': 'New Name'},
                     headers=jwt_headers)
    assert res.status_code == 404

def test_delete_nonexistent_offer_status(client, jwt_headers):
    res = client.delete('/api/status-offers/9999', headers=jwt_headers)
    assert res.status_code == 404

def test_get_all_with_status_filter(client, db, jwt_headers):
    with client.application.app_context():
        db.session.add(OfferStatus(name="Active", status=True))
        db.session.add(OfferStatus(name="Inactive", status=False))
        db.session.commit()
    # Filtrar solo activos
    res = client.get('/api/status-offers?status=true', headers=jwt_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    for status in data['data']:
        assert status['status'] == True
