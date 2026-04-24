import pytest
import json
import os
from app import create_app
from app.core.extensions import db as _db
from app.api.register_and_assign_ownership.models import Property, PropertyStatus, Client, Agent
from app.api.offers.models import Offer, OfferStatus

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
        
        status_1 = PropertyStatus(id=1, name="DISPONIBLE")
        status_2 = PropertyStatus(id=2, name="ASIGNADA")
        status_3 = PropertyStatus(id=3, name="VENDIDA")
        status_4 = PropertyStatus(id=4, name="ALQUILADA")
        offer_status_1 = OfferStatus(id=1, name="PENDIENTE")
        offer_status_2 = OfferStatus(id=2, name="ACEPTADA")
        offer_status_3 = OfferStatus(id=3, name="RECHAZADA")
        offer_status_4 = OfferStatus(id=4, name="CANCELADA")
        client_obj = Client(id=1, name="Juan Vendedor", email="juan@example.com")
        agent_obj = Agent(id=1, name="Agente 007")
        _db.session.add_all([status_1, status_2, status_3, status_4, offer_status_1, offer_status_2, offer_status_3, offer_status_4, client_obj, agent_obj])
        _db.session.commit()
        
        yield _db
        
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def available_property(db):
    """Propiedad en estado DISPONIBLE."""
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

@pytest.fixture
def assigned_property(db):
    """Propiedad en estado ASIGNADA."""
    prop = Property(
        id=2,
        type="Apartamento",
        location="Madrid",
        price_min=150000,
        price_max=180000,
        living_space_min=60,
        living_space_max=75,
        rooms=2,
        bathrooms=1,
        client_id=1,
        status_id=2,
        agent_id=1
    )
    db.session.add(prop)
    db.session.commit()
    return prop

@pytest.fixture
def sold_property(db):
    """Propiedad en estado VENDIDA."""
    prop = Property(
        id=3,
        type="Piso",
        location="Barcelona",
        price_min=200000,
        price_max=250000,
        living_space_min=70,
        living_space_max=90,
        rooms=3,
        bathrooms=2,
        client_id=1,
        status_id=3
    )
    db.session.add(prop)
    db.session.commit()
    return prop

# --- ESCENARIO 1: Registrar oferta de compra ---
def test_create_offer_compra_success(client, available_property):
    """Escenario 1: POST oferta de compra exitosa returns 201."""
    payload = {
        "type": "COMPRA",
        "offered_price": 115000,
        "property_id": 1,
        "client_id": 1,
        "agent_id": 1
    }
    res = client.post('/offers', json=payload)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['type'] == "COMPRA"
    assert data['status'] == "PENDIENTE"

# --- ESCENARIO 2: Registrar oferta de alquiler ---
def test_create_offer_alquiler_success(client, available_property):
    """Escenario 2: POST oferta de alquiler exitosa returns 201."""
    payload = {
        "type": "ALQUILER",
        "offered_price": 800,
        "property_id": 1,
        "client_id": 1
    }
    res = client.post('/offers', json=payload)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['type'] == "ALQUILER"
    assert data['status'] == "PENDIENTE"

# --- ESCENARIO 3: Validar propiedad no disponible ---
def test_create_offer_property_not_available(client, sold_property):
    """Escenario 3: POST oferta en propiedad VENDIDA returns 409."""
    payload = {
        "type": "COMPRA",
        "offered_price": 220000,
        "property_id": 3,
        "client_id": 1
    }
    res = client.post('/offers', json=payload)
    assert res.status_code == 409

# --- ESCENARIO 4: Consultar ofertas por propiedad ---
def test_get_offers_by_property(client, available_property, db):
    """Escenario 4: GET /properties/{id}/offers returns list."""
    offer = Offer(
        type="COMPRA",
        offered_price=110000,
        status_id=1,
        property_id=1,
        client_id=1
    )
    db.session.add(offer)
    db.session.commit()
    
    res = client.get('/properties/1/offers')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) == 1

# --- ESCENARIO 5: Aceptar oferta de compra (propiedad -> VENDIDA) ---
def test_accept_offer_compra_updates_property(client, available_property, db):
    """Escenario 5: PATCH aceptar oferta compra -> propiedad VENDIDA."""
    offer = Offer(
        type="COMPRA",
        offered_price=110000,
        status_id=1,
        property_id=1,
        client_id=1
    )
    db.session.add(offer)
    db.session.commit()
    offer_id = offer.id
    
    res = client.patch(f'/offers/{offer_id}/status', json={"status_id": 2})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == "ACEPTADA"
    
    prop_res = client.get('/register_and_assign_ownership/properties/1')
    prop_data = json.loads(prop_res.data)
    assert prop_data['status_id'] == 3  # VENDIDA

# --- ESCENARIO 6: Aceptar oferta de alquiler (propiedad -> ALQUILADA) ---
def test_accept_offer_alquiler_updates_property(client, assigned_property, db):
    """Escenario 6: PATCH aceptar oferta alquiler -> propiedad ALQUILADA."""
    offer = Offer(
        type="ALQUILER",
        offered_price=900,
        status_id=1,
        property_id=2,
        client_id=1
    )
    db.session.add(offer)
    db.session.commit()
    offer_id = offer.id
    
    res = client.patch(f'/offers/{offer_id}/status', json={"status_id": 2})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == "ACEPTADA"
    
    prop_res = client.get('/register_and_assign_ownership/properties/2')
    prop_data = json.loads(prop_res.data)
    assert prop_data['status_id'] == 4  # ALQUILADA

# --- ESCENARIO 7: Rechazar o cancelar oferta ---
def test_reject_offer_does_not_change_property(client, available_property, db):
    """Escenario 7: PATCH rechazar oferta -> propiedad sin cambios."""
    offer = Offer(
        type="COMPRA",
        offered_price=110000,
        status_id=1,
        property_id=1,
        client_id=1
    )
    db.session.add(offer)
    db.session.commit()
    offer_id = offer.id
    
    res = client.patch(f'/offers/{offer_id}/status', json={"status_id": 3})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == "RECHAZADA"
    
    prop_res = client.get('/register_and_assign_ownership/properties/1')
    prop_data = json.loads(prop_res.data)
    assert prop_data['status_id'] == 1  # DISPONIBLE (sin cambios)

def test_cancel_offer_does_not_change_property(client, available_property, db):
    """Escenario 7b: PATCH cancelar oferta -> propiedad sin cambios."""
    offer = Offer(
        type="ALQUILER",
        offered_price=850,
        status_id=1,
        property_id=1,
        client_id=1
    )
    db.session.add(offer)
    db.session.commit()
    offer_id = offer.id
    
    res = client.patch(f'/offers/{offer_id}/status', json={"status_id": 4})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == "CANCELADA"
    
    prop_res = client.get('/register_and_assign_ownership/properties/1')
    prop_data = json.loads(prop_res.data)
    assert prop_data['status_id'] == 1  # DISPONIBLE (sin cambios)