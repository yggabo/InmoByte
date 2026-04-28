from app.core.extensions import db
from app.api.clients.models import Client


def get_all_clients():
    return Client.query.filter(Client.status == True).all()


def get_client_by_id(client_id):
    return Client.query.filter(
        Client.id == client_id,
        Client.status == True
    ).first()


def get_client_by_email(email):
    return Client.query.filter(
        Client.email == email,
        Client.status == True
    ).first()


def create_client(data):
    client = Client(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        age=data.get('age'),
        status=True
    )
    db.session.add(client)
    db.session.commit()
    return client


def update_client(client_id, data):
    client = db.session.get(Client, client_id)
    if not client:
        return None

    if 'email' in data:
        existing = Client.query.filter(
            Client.email == data['email'],
            Client.id != client_id,
            Client.status == True
        ).first()
        if existing:
            return False
        client.email = data['email']

    if 'name' in data:
        client.name = data['name']

    if 'phone' in data:
        client.phone = data['phone']

    if 'address' in data:
        client.address = data['address']

    if 'age' in data:
        client.age = data['age']

    db.session.commit()
    return client


def delete_client(client_id):
    client = db.session.get(Client, client_id)
    if not client:
        return None

    client.status = False
    db.session.commit()
    return client