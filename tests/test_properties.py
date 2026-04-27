import pytest
import json
import os
from app import create_app
from app.core.extensions import db as _db
from app.api.register_and_assign_ownership.models import Property, PropertyStatus, Agent
from app.api.clients.models import Client
from app.api.auth.models import Users

# --- FIXTURES ---

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
        
        from app.core.extensions import bcrypt
        
        # Datos base necesarios para las pruebas
        status_1 = PropertyStatus(id=1, name="DISPONIBLE")
        status_2 = PropertyStatus(id=2, name="ASIGNADA")
        client_obj = Client(id=1, name="Juan Vendedor", email="juan@example.com")
        agent_obj = Agent(id=1, name="Agente 007")
        
        # Usuario para JWT
        user = Users(
            id=1,
            username="testuser",
            email="test@example.com",
            password_hash=bcrypt.generate_password_hash("password123").decode('utf-8')
        )
        
        _db.session.add_all([status_1, status_2, client_obj, agent_obj, user])
        _db.session.commit()
        
        yield _db
        
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def auth_headers(client, db):
    """Headers con token JWT."""
    res = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    data = json.loads(res.data)
    token = data['data']['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_property(db):
    """Crea una propiedad inicial para pruebas de detalle, actualización y borrado."""
    prop = Property(
        id=1,
        type="Casa",
        location="Valencia",
        price_min=100000,
        price_max=120000,
        living_space_min=80,
        living_space_max=100,
        rooms=3,
        bathrooms=2,
        client_id=1,
        status_id=1
    )
    db.session.add(prop)
    db.session.commit()
    return prop

# --- TESTS ---

def test_get_all_properties(client, sample_property, auth_headers):
    """Verificar que el listado de propiedades funciona."""
    res = client.get('/register_and_assign_ownership/properties', headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_property_detail(client, sample_property, auth_headers):
    """Verificar que se obtiene el detalle de una propiedad específica."""
    res = client.get('/register_and_assign_ownership/properties/1', headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['location'] == "Valencia"

def test_create_property_success(client, db, auth_headers):
    """Verificar el registro de una nueva propiedad."""
    payload = {
        "type": "Apartamento",
        "location": "Madrid",
        "price_min": 150000,
        "price_max": 180000,
        "living_space_min": 60,
        "living_space_max": 75,
        "rooms": 2,
        "bathrooms": 1,
        "client_id": 1,
        "status_id": 1
    }
    res = client.post('/register_and_assign_ownership/properties', json=payload, headers=auth_headers)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['location'] == "Madrid"

def test_update_property_partial(client, sample_property, auth_headers):
    """Verificar que la actualización parcial funciona."""
    payload = {"price_max": 130000}
    res = client.put('/register_and_assign_ownership/properties/1', json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert float(data['price_max']) == 130000.0
    assert data['location'] == "Valencia"

def test_delete_property(client, sample_property, auth_headers):
    """Verificar que se puede eliminar una propiedad."""
    res = client.delete('/register_and_assign_ownership/properties/1', headers=auth_headers)
    assert res.status_code == 200
    
    res_get = client.get('/register_and_assign_ownership/properties/1', headers=auth_headers)
    assert res_get.status_code == 404

def test_assign_agent_success(client, sample_property, auth_headers):
    """Verificar la asignación de un agente."""
    payload = {"agent_id": 1}
    res = client.patch('/register_and_assign_ownership/properties/1/assign-agent', json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['agent_id'] == 1
    assert data['status_id'] == 2