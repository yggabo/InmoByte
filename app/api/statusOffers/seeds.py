from app.core.extensions import db
from sqlalchemy import inspect
from app.api.statusOffers.models import OfferStatus

def seed_offer_status():
    
    existing_status = OfferStatus.query.count()
    if existing_status == 0:
        statuses = [
            OfferStatus(name='Pendiente'),
            OfferStatus(name='Aceptada'),
            OfferStatus(name='Rechazada'),
            OfferStatus(name='Cancelada')
        ]
        db.session.bulk_save_objects(statuses)
        db.session.commit()