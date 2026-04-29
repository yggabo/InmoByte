from app.core.extensions import db
from app.api.propertyStatus.models import PropertyStatus
from sqlalchemy import inspect


def seed_property_statuses():
    inspector = inspect(db.engine)
    if not inspector.has_table('property_status'):
        return
    
    # Define statuses with their accepts_offers flag
    statuses_data = [
        ("en venta", True),
        ("en alquiler", True),
        ("reservado", False),
        ("vendido", False),
        ("alquilado", False)
    ]
    
    existing = PropertyStatus.query.filter(
        PropertyStatus.name.in_([name for name, _ in statuses_data])
    ).count()
    
    if existing == 0:
        status_objects = [
            PropertyStatus(name=name, status=True, accepts_offers=accepts_offers)
            for name, accepts_offers in statuses_data
        ]
        db.session.bulk_save_objects(status_objects)
        db.session.commit()
