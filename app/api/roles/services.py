from app.core.extensions import db
from app.api.roles.models import Roles


def get_all_roles():
    return Roles.query.filter(Roles.status == True).all()


def get_role_by_id(role_id):
    return Roles.query.filter(
        Roles.id == role_id,
        Roles.status == True
    ).first()


def get_role_by_name(name):
    return Roles.query.filter(
        Roles.name == name,
        Roles.status == True
    ).first()


def create_role(name):
    role = Roles(name=name, status=True)
    db.session.add(role)
    db.session.commit()
    return role


def update_role(role_id, data):
    role = db.session.get(Roles, role_id)
    if not role:
        return None

    if 'name' in data:
        existing = Roles.query.filter(
            Roles.name == data['name'],
            Roles.id != role_id
        ).first()
        if existing:
            return False
        role.name = data['name']

    if 'status' in data:
        role.status = data['status']

    db.session.commit()
    return role


def delete_role(role_id):
    role = db.session.get(Roles, role_id)
    if not role:
        return None

    role.status = False
    db.session.commit()
    return role