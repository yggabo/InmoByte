#!/usr/bin/env python3
"""Script para poblar la base de datos con datos de demo."""

from app import create_app
from app.core.extensions import db, bcrypt
from app.api.auth.models import Users
from app.api.roles.models import Roles
from app.api.userProfile.models import UserProfile
from app.api.clients.models import Client
from app.api.agents.models import Agent
from app.api.propertyStatus.models import PropertyStatus
from app.api.statusOffers.models import OfferStatus
from app.api.appointments_scheduling.models import AppointmentStatus, Appointment
from app.api.register_and_assign_ownership.models import Property
from app.api.offers.models import Offer
from app.api.preferences.models import Preference
from datetime import datetime, date, time, timedelta
import random

def seed_demo_data():
    app = create_app('dev')
    
    with app.app_context():
        print("=== Iniciando seeding de datos para demo ===")
        
        if Users.query.filter(Users.email.like('%@inmobyte.com')).count() > 0:
            print("Los datos de demo ya existen. Saltando...")
            return
        
        # Obtener roles existentes
        admin_role = Roles.query.filter_by(name='admin').first()
        agente_role = Roles.query.filter_by(name='agente').first()
        
        if not admin_role or not agente_role:
            print("Error: Roles no encontrados. Asegúrate de que la app se haya iniciado al menos una vez.")
            return
        
        # Obtener estados existentes
        property_statuses = {ps.name: ps for ps in PropertyStatus.query.all()}
        offer_statuses = {os.name: os for os in OfferStatus.query.all()}
        appointment_statuses = {as_.name: as_ for as_ in AppointmentStatus.query.all()}
        
        print("[1/9] Creando usuarios...")
        users_data = [
            {'email': 'admin@inmobyte.com', 'username': 'admin', 'password': 'admin123', 'role': admin_role},
            {'email': 'agente1@inmobyte.com', 'username': 'agente1', 'password': 'agente123', 'role': agente_role},
            {'email': 'agente2@inmobyte.com', 'username': 'agente2', 'password': 'agente123', 'role': agente_role},
        ]
        
        users = []
        for u_data in users_data:
            user = Users(
                email=u_data['email'],
                username=u_data['username'],
                password_hash=bcrypt.generate_password_hash(u_data['password']).decode('utf-8')
            )
            users.append(user)
        
        db.session.bulk_save_objects(users)
        db.session.commit()
        users = Users.query.filter(Users.email.like('%@inmobyte.com')).all()
        
        print("[2/9] Creando perfiles de usuario...")
        profiles_data = [
            {'user': users[0], 'name': 'Administrador', 'lastNames': 'Sistema', 'role': admin_role, 'phone': '600000001'},
            {'user': users[1], 'name': 'Carlos', 'lastNames': 'Martínez López', 'role': agente_role, 'phone': '600000002'},
            {'user': users[2], 'name': 'Ana', 'lastNames': 'García Ruiz', 'role': agente_role, 'phone': '600000003'},
        ]
        
        profiles = []
        for p_data in profiles_data:
            profile = UserProfile(
                name=p_data['name'],
                lastNames=p_data['lastNames'],
                telefono=p_data['phone'],
                rolId=p_data['role'].id,
                userId=p_data['user'].id
            )
            profiles.append(profile)
        
        db.session.bulk_save_objects(profiles)
        db.session.commit()
        
        print("[3/9] Creando clientes...")
        clients_data = [
            {'name': 'Juan Pérez García', 'email': 'juan.perez@email.com', 'phone': '611111111', 'address': 'Calle Mayor 123, Madrid', 'age': 35},
            {'name': 'María García López', 'email': 'maria.garcia@email.com', 'phone': '622222222', 'address': 'Avenida Sol 45, Barcelona', 'age': 28},
            {'name': 'Carlos López Martín', 'email': 'carlos.lopez@email.com', 'phone': '633333333', 'address': 'Plaza Luna 7, Valencia', 'age': 42},
            {'name': 'Laura Ruiz Sánchez', 'email': 'laura.ruiz@email.com', 'phone': '644444444', 'address': 'Calle Estrella 89, Madrid', 'age': 31},
            {'name': 'David Sánchez Torres', 'email': 'david.sanchez@email.com', 'phone': '655555555', 'address': 'Gran Vía 12, Barcelona', 'age': 38},
            {'name': 'Elena Torres Vega', 'email': 'elena.torres@email.com', 'phone': '666666666', 'address': 'Calle Mar 34, Valencia', 'age': 29},
            {'name': 'Miguel Vega Romero', 'email': 'miguel.vega@email.com', 'phone': '677777777', 'address': 'Avenida Paz 56, Madrid', 'age': 45},
            {'name': 'Cristina Romero Díaz', 'email': 'cristina.romero@email.com', 'phone': '688888888', 'address': 'Calle Río 21, Barcelona', 'age': 33},
        ]
        
        clients = []
        for c_data in clients_data:
            client = Client(
                name=c_data['name'],
                email=c_data['email'],
                phone=c_data['phone'],
                address=c_data['address'],
                age=c_data['age'],
                status=True
            )
            clients.append(client)
        
        db.session.bulk_save_objects(clients)
        db.session.commit()
        clients = Client.query.all()
        
        print("[4/9] Creando agentes...")
        profiles = UserProfile.query.filter(UserProfile.rolId == agente_role.id).all()
        
        agents = []
        for profile in profiles:
            agent = Agent(
                userProfileId=profile.id,
                status=True
            )
            agents.append(agent)
        
        db.session.bulk_save_objects(agents)
        db.session.commit()
        agents = Agent.query.all()
        
        print("[5/9] Creando propiedades...")
        properties_data = [
            {'type': 'Apartamento', 'location': 'Madrid Centro', 'price_min': 250000, 'price_max': 300000, 'living_space': 85.5, 'rooms': 3, 'bathrooms': 2, 'description': 'Apartamento reformado en zona céntrica', 'status': 'en venta', 'client': clients[0]},
            {'type': 'Casa', 'location': 'Barcelona Eixample', 'price_min': 400000, 'price_max': 450000, 'living_space': 120.0, 'rooms': 4, 'bathrooms': 3, 'description': 'Casa unifamiliar con jardín', 'status': 'en venta', 'client': clients[1]},
            {'type': 'Apartamento', 'location': 'Valencia Playa', 'price_min': 180000, 'price_max': 220000, 'living_space': 65.0, 'rooms': 2, 'bathrooms': 1, 'description': 'Apartamento cerca de la playa', 'status': 'en alquiler', 'client': clients[2]},
            {'type': 'Ático', 'location': 'Madrid Salamanca', 'price_min': 500000, 'price_max': 550000, 'living_space': 110.0, 'rooms': 3, 'bathrooms': 2, 'description': 'Ático de lujo con terraza', 'status': 'en venta', 'client': clients[3]},
            {'type': 'Local', 'location': 'Barcelona Gracia', 'price_min': 150000, 'price_max': 180000, 'living_space': 95.0, 'rooms': 1, 'bathrooms': 1, 'description': 'Local comercial en zona transitada', 'status': 'en alquiler', 'client': clients[4]},
            {'type': 'Apartamento', 'location': 'Madrid Chamberí', 'price_min': 320000, 'price_max': 350000, 'living_space': 90.0, 'rooms': 3, 'bathrooms': 2, 'description': 'Apartamento luminoso con balcón', 'status': 'vendido', 'client': clients[0], 'agent': agents[0]},
            {'type': 'Casa', 'location': 'Valencia Ciudad', 'price_min': 280000, 'price_max': 320000, 'living_space': 100.0, 'rooms': 3, 'bathrooms': 2, 'description': 'Casa con piscina comunitaria', 'status': 'en venta', 'client': clients[5]},
            {'type': 'Apartamento', 'location': 'Barcelona Born', 'price_min': 350000, 'price_max': 380000, 'living_space': 75.0, 'rooms': 2, 'bathrooms': 2, 'description': 'Apartamento moderno en edificio histórico', 'status': 'reservado', 'client': clients[1], 'agent': agents[1]},
            {'type': 'Estudio', 'location': 'Madrid Tetuán', 'price_min': 120000, 'price_max': 150000, 'living_space': 40.0, 'rooms': 1, 'bathrooms': 1, 'description': 'Estudio reformado ideal inversión', 'status': 'en venta', 'client': clients[6]},
            {'type': 'Apartamento', 'location': 'Valencia Patraix', 'price_min': 160000, 'price_max': 190000, 'living_space': 70.0, 'rooms': 2, 'bathrooms': 1, 'description': 'Apartamento bien comunicado', 'status': 'en alquiler', 'client': clients[7]},
            {'type': 'Casa', 'location': 'Barcelona Sant Gervasi', 'price_min': 600000, 'price_max': 650000, 'living_space': 150.0, 'rooms': 5, 'bathrooms': 4, 'description': 'Casa señorial con jardín privado', 'status': 'en venta', 'client': clients[3], 'agent': agents[0]},
            {'type': 'Apartamento', 'location': 'Madrid Latina', 'price_min': 200000, 'price_max': 230000, 'living_space': 80.0, 'rooms': 3, 'bathrooms': 2, 'description': 'Apartamento familiar cerca de parques', 'status': 'alquilado', 'client': clients[4], 'agent': agents[1]},
        ]
        
        properties = []
        for p_data in properties_data:
            status = property_statuses.get(p_data['status'])
            if not status:
                continue
            
            prop = Property(
                type=p_data['type'],
                location=p_data['location'],
                price_min=p_data['price_min'],
                price_max=p_data['price_max'],
                living_space=p_data['living_space'],
                rooms=p_data['rooms'],
                bathrooms=p_data['bathrooms'],
                description=p_data['description'],
                client_id=p_data['client'].id,
                agent_id=p_data.get('agent').id if p_data.get('agent') else None,
                status_id=status.id
            )
            properties.append(prop)
        
        db.session.bulk_save_objects(properties)
        db.session.commit()
        properties = Property.query.all()
        
        print("[6/9] Creando ofertas...")
        offers_data = [
            {'offered_price': 280000, 'property': properties[0], 'client': clients[1], 'status': 'Pendiente'},
            {'offered_price': 420000, 'property': properties[1], 'client': clients[3], 'status': 'Aceptada'},
            {'offered_price': 200000, 'property': properties[2], 'client': clients[0], 'status': 'Rechazada'},
            {'offered_price': 480000, 'property': properties[3], 'client': clients[5], 'status': 'Pendiente'},
            {'offered_price': 300000, 'property': properties[4], 'client': clients[6], 'status': 'Cancelada'},
        ]
        
        offers = []
        for o_data in offers_data:
            status = offer_statuses.get(o_data['status'])
            if not status:
                continue
            
            offer = Offer(
                offered_price=o_data['offered_price'],
                property_id=o_data['property'].id,
                client_id=o_data['client'].id,
                status_id=status.id
            )
            offers.append(offer)
        
        db.session.bulk_save_objects(offers)
        db.session.commit()
        
        print("[7/9] Creando citas...")
        base_date = date.today()
        appointments_data = [
            {'date': base_date - timedelta(days=10), 'start': time(10, 0), 'end': time(11, 0), 'client': clients[0], 'property': properties[0], 'agent': agents[0], 'status': 'REALIZADA', 'notes': 'Primera visita al apartamento'},
            {'date': base_date - timedelta(days=5), 'start': time(16, 0), 'end': time(17, 0), 'client': clients[1], 'property': properties[1], 'agent': agents[1], 'status': 'REALIZADA', 'notes': 'Visita casa con jardín'},
            {'date': base_date + timedelta(days=2), 'start': time(11, 0), 'end': time(12, 0), 'client': clients[2], 'property': properties[2], 'agent': agents[0], 'status': 'PROGRAMADA', 'notes': 'Ver apartamento cerca playa'},
            {'date': base_date + timedelta(days=5), 'start': time(17, 0), 'end': time(18, 0), 'client': clients[3], 'property': properties[3], 'agent': agents[1], 'status': 'PROGRAMADA', 'notes': 'Visita ático de lujo'},
            {'date': base_date - timedelta(days=3), 'start': time(12, 0), 'end': time(13, 0), 'client': clients[4], 'property': properties[5], 'agent': agents[0], 'status': 'CANCELADA', 'notes': 'Cliente no pudo asistir'},
            {'date': base_date + timedelta(days=7), 'start': time(10, 30), 'end': time(11, 30), 'client': clients[5], 'property': properties[6], 'agent': agents[1], 'status': 'PROGRAMADA', 'notes': 'Ver casa con piscina'},
            {'date': base_date - timedelta(days=15), 'start': time(18, 0), 'end': time(19, 0), 'client': clients[6], 'property': properties[8], 'agent': agents[0], 'status': 'NOSHOW', 'notes': 'Cliente no se presentó'},
        ]
        
        appointments = []
        for a_data in appointments_data:
            status = appointment_statuses.get(a_data['status'])
            if not status:
                continue
            
            appointment = Appointment(
                appointment_date=a_data['date'],
                start_time=a_data['start'],
                end_time=a_data['end'],
                notes=a_data['notes'],
                is_active=True,
                client_id=a_data['client'].id,
                property_id=a_data['property'].id,
                agent_id=a_data['agent'].id,
                status_id=status.id
            )
            appointments.append(appointment)
        
        db.session.bulk_save_objects(appointments)
        db.session.commit()
        
        print("[8/9] Creando preferencias...")
        preferences_data = [
            {'client': clients[0], 'property_type': 'Apartamento', 'price_min': 200000, 'price_max': 300000, 'location': 'Madrid', 'bedrooms': 3, 'bathrooms': 2, 'living_min': 80, 'living_max': 100},
            {'client': clients[1], 'property_type': 'Casa', 'price_min': 350000, 'price_max': 500000, 'location': 'Barcelona', 'bedrooms': 4, 'bathrooms': 3, 'living_min': 100, 'living_max': 150},
            {'client': clients[2], 'property_type': 'Apartamento', 'price_min': 150000, 'price_max': 250000, 'location': 'Valencia', 'bedrooms': 2, 'bathrooms': 1, 'living_min': 60, 'living_max': 80},
            {'client': clients[3], 'property_type': 'Ático', 'price_min': 450000, 'price_max': 600000, 'location': 'Madrid', 'bedrooms': 3, 'bathrooms': 2, 'living_min': 100, 'living_max': 130},
        ]
        
        preferences = []
        for p_data in preferences_data:
            pref = Preference(
                client_id=p_data['client'].id,
                property_type_id=None,
                price_min=p_data['price_min'],
                price_max=p_data['price_max'],
                location=p_data['location'],
                bedrooms=p_data['bedrooms'],
                bathrooms=p_data['bathrooms'],
                living_space_min=p_data['living_min'],
                living_space_max=p_data['living_max']
            )
            preferences.append(pref)
        
        db.session.bulk_save_objects(preferences)
        db.session.commit()
        
        print("[9/9] Verificando datos insertados...")
        print(f"  - Users: {Users.query.count()}")
        print(f"  - UserProfiles: {UserProfile.query.count()}")
        print(f"  - Clients: {Client.query.count()}")
        print(f"  - Agents: {Agent.query.count()}")
        print(f"  - Properties: {Property.query.count()}")
        print(f"  - Offers: {Offer.query.count()}")
        print(f"  - Appointments: {Appointment.query.count()}")
        print(f"  - Preferences: {Preference.query.count()}")
        
        print("=== Seeding completado exitosamente ===")

if __name__ == '__main__':
    seed_demo_data()
