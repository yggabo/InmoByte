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

def seed_offer_status():
    from app.api.register_and_assign_ownership.models import PropertyStatus
    from app.api.offers.models import OfferStatus, OfferType
    
    existing_status = OfferStatus.query.count()
    if existing_status == 0:
        statuses = [
            OfferStatus(name='PENDIENTE'),
            OfferStatus(name='ACEPTADA'),
            OfferStatus(name='RECHAZADA'),
            OfferStatus(name='CANCELADA')
        ]
        db.session.bulk_save_objects(statuses)
        db.session.commit()
    
    existing_type = OfferType.query.count()
    if existing_type == 0:
        types = [
            OfferType(name='COMPRA'),
            OfferType(name='ALQUILER')
        ]
        db.session.bulk_save_objects(types)
        db.session.commit()