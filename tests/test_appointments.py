import pytest
import json
import os
from app import create_app
from app.core.extensions import db as _db
from app.api.appointments_scheduling.models import Appointment, AppointmentStatus
from app.api.register_and_assign_ownership.models import Property, PropertyStatus
from app.api.agents.models import Agent
from app.api.clients.models import Client
from app.api.auth.models import Users
from datetime import date, time

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
        
        # 1. Estados de Propiedad
        if not PropertyStatus.query.get(1):
            _db.session.add(PropertyStatus(id=1, name="DISPONIBLE"))
        if not PropertyStatus.query.get(2):
            _db.session.add(PropertyStatus(id=2, name="ASIGNADA"))
        
        # 2. Estados de Cita
        if not AppointmentStatus.query.filter_by(name='PROGRAMADA').first():
            _db.session.add(AppointmentStatus(name='PROGRAMADA', description='Cita programada'))
        if not AppointmentStatus.query.filter_by(name='REALIZADA').first():
            _db.session.add(AppointmentStatus(name='REALIZADA', description='Cita realizada'))
        
        # 3. Cliente
        if not Client.query.get(1):
            _db.session.add(Client(id=1, name="Juan Perez", email="juan@example.com"))
        
        # 4. Agente (Usuario -> Perfil -> Agente)
        rol = Roles.query.filter_by(name='agente').first()
        if not rol:
            rol = Roles(id=1, name='agente', status=True)
            _db.session.add(rol)
        
        user = Users.query.filter_by(username='testagent').first()
        if not user:
            user = Users(
                id=1,
                username="testagent",
                email="agent@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8')
            )
            _db.session.add(user)
        
        profile = UserProfile.query.filter_by(userId=1).first()
        if not profile:
            profile = UserProfile(id=1, name="Agente", lastNames="Test", telefono="123456", rolId=1, userId=1)
            _db.session.add(profile)
            
        agent = Agent.query.filter_by(userProfileId=1).first()
        if not agent:
            agent = Agent(id=1, userProfileId=1, status=True)
            _db.session.add(agent)
            
        # 5. Propiedad
        prop = Property.query.get(1)
        if not prop:
            prop = Property(
                id=1, type="Casa", location="Valencia", price_min=100, price_max=200,
                living_space_min=50, living_space_max=100, rooms=2, bathrooms=1,
                client_id=1, status_id=2, agent_id=1
            )
            _db.session.add(prop)
        
        _db.session.commit()
        
        yield _db
        
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def auth_headers(client, db):
    """Headers con token JWT."""
    res = client.post('/api/auth/login', json={
        'username': 'testagent',
        'password': 'password123'
    })
    data = json.loads(res.data)
    token = data['data']['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_appointment(db):
    """Crea una cita inicial."""
    status = AppointmentStatus.query.filter_by(name='PROGRAMADA').first()
    appt = Appointment(
        appointment_date=date(2026, 5, 10),
        start_time=time(10, 0),
        end_time=time(11, 0),
        client_id=1,
        property_id=1,
        agent_id=1,
        status_id=status.id,
        notes="Cita de prueba"
    )
    db.session.add(appt)
    db.session.commit()
    return appt

# --- TESTS ---

def test_create_appointment_success(client, db, auth_headers):
    payload = {
        "appointment_date": "2026-05-12",
        "start_time": "14:00:00",
        "end_time": "15:00:00",
        "client_id": 1,
        "property_id": 1,
        "notes": "Interesado en la terraza"
    }
    res = client.post('/appointments', json=payload, headers=auth_headers)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['data']['client_name'] == "Juan Perez"
    assert data['data']['status_name'] == "PROGRAMADA"

def test_create_appointment_conflict(client, sample_appointment, auth_headers):
    payload = {
        "appointment_date": "2026-05-10",
        "start_time": "10:30:00",
        "end_time": "11:30:00",
        "client_id": 1,
        "property_id": 1,
        "agent_id": 1
    }
    res = client.post('/appointments', json=payload, headers=auth_headers)
    assert res.status_code == 409
    data = json.loads(res.data)
    assert "cita programada" in data['message']

def test_list_appointments(client, sample_appointment, auth_headers):
    res = client.get('/appointments', headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data['data']) >= 1

def test_update_appointment_status(client, sample_appointment, auth_headers):
    status_realizada = AppointmentStatus.query.filter_by(name='REALIZADA').first()
    payload = {"status_id": status_realizada.id}
    res = client.put(f'/appointments/{sample_appointment.id}', json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['data']['status_name'] == "REALIZADA"

def test_delete_appointment(client, sample_appointment, auth_headers):
    res = client.delete(f'/appointments/{sample_appointment.id}', headers=auth_headers)
    assert res.status_code == 200
    
    # Verificar que ya no aparece en el listado
    res_list = client.get('/appointments', headers=auth_headers)
    data = json.loads(res_list.data)
    assert all(a['id'] != sample_appointment.id for a in data['data'])

def test_get_property_appointments(client, sample_appointment, auth_headers):
    res = client.get('/register_and_assign_ownership/properties/1/appointments', headers=auth_headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data) >= 1
    assert data[0]['property_location'] == "Valencia"
