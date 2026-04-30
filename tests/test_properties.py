import pytest
import json
import os
from app import create_app
from app.core.extensions import db as _db
from app.api.register_and_assign_ownership.models import Property, PropertyStatus
from app.api.agents.models import Agent
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
        from app.api.userProfile.models import UserProfile
        from app.api.roles.models import Roles
        
        # Verificar si el status ya existe
        status_1 = PropertyStatus.query.filter(PropertyStatus.id == 1).first()
        if not status_1:
            status_1 = PropertyStatus(id=1, name="DISPONIBLE")
            _db.session.add(status_1)
        
        status_2 = PropertyStatus.query.filter(PropertyStatus.id == 2).first()
        if not status_2:
            status_2 = PropertyStatus(id=2, name="ASIGNADA")
            _db.session.add(status_2)
        
        # Verificar si el cliente ya existe
        client_obj = Client.query.filter(Client.id == 1).first()
        if not client_obj:
            client_obj = Client(id=1, name="Juan Vendedor", email="juan@example.com")
            _db.session.add(client_obj)
        
        # Verificar si el rol ya existe (del seed)
        rol = Roles.query.filter(Roles.name == 'agente').first()
        if not rol:
            rol = Roles(id=1, name='agente', status=True)
            _db.session.add(rol)
        
        # Verificar si el usuario ya existe
        user = Users.query.filter(Users.username == 'testuser').first()
        if not user:
            user = Users(
                id=1,
                username="testuser",
                email="test@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8')
            )
            _db.session.add(user)
        
        # Verificar si el userProfile ya existe
        userProfile = UserProfile.query.filter(UserProfile.userId == 1).first()
        if not userProfile:
            userProfile = UserProfile(
                id=1,
                name="Agente",
                lastNames="007",
                telefono="1234567890",
                rolId=rol.id,
                userId=1
            )
            _db.session.add(userProfile)
        
        # Verificar si el agente ya existe
        from app.api.agents.models import Agent
        agent_obj = Agent.query.filter(Agent.userProfileId == 1).first()
        if not agent_obj:
            agent_obj = Agent(id=1, userProfileId=1, status=True)
            _db.session.add(agent_obj)
        
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
        living_space=90,
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
    res = client.get('/api/register-and-assign-ownership/properties', headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_property_detail(client, sample_property, auth_headers):
    """Verificar que se obtiene el detalle de una propiedad específica."""
    res = client.get('/api/register-and-assign-ownership/properties/1', headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['location'] == "Valencia"
    # Verificar que la respuesta incluye cliente, status y agente
    assert 'client' in data
    assert 'status' in data
    assert 'agent' in data
    # Cliente debería estar presente
    assert data['client'] is not None
    assert data['client']['id'] == 1
    # Status debería estar presente
    assert data['status'] is not None
    assert data['status']['id'] == 1
    # Agent no debería estar asignado aún
    assert data['agent'] is None

def test_create_property_success(client, db, auth_headers):
    """Verificar el registro de una nueva propiedad."""
    payload = {
        "type": "Apartamento",
        "location": "Madrid",
        "price_min": 150000,
        "price_max": 180000,
        "living_space": 70,
        "rooms": 2,
        "bathrooms": 1,
        "client_id": 1,
        "status_id": 1
    }
    res = client.post('/api/register-and-assign-ownership/properties', json=payload, headers=auth_headers)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['location'] == "Madrid"

def test_update_property_partial(client, sample_property, auth_headers):
    """Verificar que la actualización parcial funciona."""
    payload = {"price_max": 130000}
    res = client.put('/api/register-and-assign-ownership/properties/1', json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert float(data['price_max']) == 130000.0
    assert data['location'] == "Valencia"

def test_delete_property(client, sample_property, auth_headers):
    """Verificar que se puede eliminar una propiedad."""
    res = client.delete('/api/register-and-assign-ownership/properties/1', headers=auth_headers)
    assert res.status_code == 200
    
    res_get = client.get('/api/register-and-assign-ownership/properties/1', headers=auth_headers)
    assert res_get.status_code == 404

def test_assign_agent_success(client, sample_property, auth_headers):
    """Verificar la asignación de un agente."""
    payload = {"agent_id": 1}
    res = client.patch('/api/register-and-assign-ownership/properties/1/assign-agent', json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['agent'] is not None
    assert data['agent']['id'] == 1
    # Verificar que el status NO cambió (follow plan - no change status)
    assert data['status']['id'] == 1