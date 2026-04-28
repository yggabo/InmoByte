from app.core.extensions import db
from app.api.roles.models import Roles
from sqlalchemy import inspect


def seed_roles():
    inspector = inspect(db.engine)
    if not inspector.has_table('roles'):
        return
    
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