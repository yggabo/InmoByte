from app.core.extensions import db
from app.api.roles.models import Roles

def seed_roles():
    existing = Roles.query.filter(
        Roles.name.in_(['admin', 'agente'])
    ).count()

    if existing == 0:
        roles = [
            Roles(name='admin', status=True),
            Roles(name='agente', status=True)
        ]
        db.session.bulk_save_objects(roles)
        db.session.commit()