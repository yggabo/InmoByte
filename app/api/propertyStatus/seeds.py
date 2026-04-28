from app.core.extensions import db
from app.api.propertyStatus.models import PropertyStatus
from sqlalchemy import inspect


def seed_property_statuses():
    inspector = inspect(db.engine)
    if not inspector.has_table('property_status'):
        return
    
    statuses = ["en venta", "en alquiler", "reservado", "vendido", "alquilado"]
    existing = PropertyStatus.query.filter(PropertyStatus.name.in_(statuses)).count()
    
    if existing == 0:
        status_objects = [PropertyStatus(name=name, status=True) for name in statuses]
        db.session.bulk_save_objects(status_objects)
        db.session.commit()
