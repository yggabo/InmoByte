import unittest
import json
import os
from app import create_app
from app.core.extensions import db
from app.api.register_and_assign_ownership.models import Property, PropertyStatus, Client, Agent

class PropertyTestCase(unittest.TestCase):
    def setUp(self):
        # Base de datos en memoria para velocidad y limpieza
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_app('test')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Datos base para las pruebas
            status_1 = PropertyStatus(id=1, name="DISPONIBLE")
            status_2 = PropertyStatus(id=2, name="ASIGNADA")
            client = Client(id=1, name="Juan Vendedor", email="juan@example.com")
            agent = Agent(id=1, name="Agente 007")
            db.session.add_all([status_1, status_2, client, agent])
            
            # Insertamos una propiedad inicial para probar GET, PUT y DELETE
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

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_properties(self):
        """Verificar que el listado de propiedades funciona"""
        res = self.client.get('/register_and_assign_ownership/properties')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_property_detail(self):
        """Verificar que se obtiene el detalle de una propiedad específica"""
        res = self.client.get('/register_and_assign_ownership/properties/1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['location'], "Valencia")

    def test_create_property_success(self):
        """Verificar el registro de una nueva propiedad"""
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
        res = self.client.post('/register_and_assign_ownership/properties', json=payload)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['location'], "Madrid")

    def test_update_property_partial(self):
        """Verificar que la actualización parcial (PUT con partial=True) funciona"""
        payload = {"price_max": 130000} # Solo cambiamos un campo
        res = self.client.put('/register_and_assign_ownership/properties/1', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(float(data['price_max']), 130000.0)
        # Verificamos que lo que no enviamos se mantiene igual
        self.assertEqual(data['location'], "Valencia")

    def test_delete_property(self):
        """Verificar que se puede eliminar una propiedad"""
        res = self.client.delete('/register_and_assign_ownership/properties/1')
        self.assertEqual(res.status_code, 200)
        # Verificamos que ya no existe
        res_get = self.client.get('/register_and_assign_ownership/properties/1')
        self.assertEqual(res_get.status_code, 404)

    def test_assign_agent_success(self):
        """Verificar la asignación de un agente"""
        payload = {"agent_id": 1}
        res = self.client.patch('/register_and_assign_ownership/properties/1/assign-agent', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['agent_id'], 1)
        self.assertEqual(data['status_id'], 2) # ASIGNADA
