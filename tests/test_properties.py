import pytest
import json
import os
from app import create_app
from app.core.extensions import db as _db
from app.api.register_and_assign_ownership.models import Property, PropertyStatus, Client, Agent

# --- FIXTURES ---

@pytest.fixture(scope='module')
def app():
    """Configuración de la aplicación para pruebas."""
    # Si no hay una URI definida en el entorno, usamos SQLite en memoria por defecto
    if not os.environ.get('SQLALCHEMY_DATABASE_URI'):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
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
        
        # Datos base necesarios para las pruebas
        status_1 = PropertyStatus(id=1, name="DISPONIBLE")
        status_2 = PropertyStatus(id=2, name="ASIGNADA")
        client_obj = Client(id=1, name="Juan Vendedor", email="juan@example.com")
        agent_obj = Agent(id=1, name="Agente 007")
        _db.session.add_all([status_1, status_2, client_obj, agent_obj])
        _db.session.commit()
        
        yield _db
        
        _db.session.remove()
        _db.drop_all()

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

def test_get_all_properties(client, sample_property):
    """Verificar que el listado de propiedades funciona."""
    res = client.get('/register_and_assign_ownership/properties')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_property_detail(client, sample_property):
    """Verificar que se obtiene el detalle de una propiedad específica."""
    res = client.get('/register_and_assign_ownership/properties/1')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['location'] == "Valencia"

def test_create_property_success(client, db):
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
    res = client.post('/register_and_assign_ownership/properties', json=payload)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['location'] == "Madrid"

def test_update_property_partial(client, sample_property):
    """Verificar que la actualización parcial funciona."""
    payload = {"price_max": 130000}
    res = client.put('/register_and_assign_ownership/properties/1', json=payload)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert float(data['price_max']) == 130000.0
    assert data['location'] == "Valencia"

def test_delete_property(client, sample_property):
    """Verificar que se puede eliminar una propiedad."""
    res = client.delete('/register_and_assign_ownership/properties/1')
    assert res.status_code == 200
    
    # Verificamos que ya no existe
    res_get = client.get('/register_and_assign_ownership/properties/1')
    assert res_get.status_code == 404

def test_assign_agent_success(client, sample_property):
    """Verificar la asignación de un agente."""
    payload = {"agent_id": 1}
    res = client.patch('/register_and_assign_ownership/properties/1/assign-agent', json=payload)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['agent_id'] == 1
    assert data['status_id'] == 2 # ASIGNADA
