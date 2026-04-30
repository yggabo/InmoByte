from app.core.extensions import db
from app.api.propertyStatus.models import PropertyStatus


def get_all_property_statuses(status_filter=None):
    query = PropertyStatus.query
    if status_filter is not None:
        query = query.filter(PropertyStatus.status == status_filter)
    return query.all()


def get_property_status_by_id(status_id):
    return PropertyStatus.query.filter(PropertyStatus.id == status_id).first()


def get_property_status_by_name(name):
    return PropertyStatus.query.filter(PropertyStatus.name == name).first()


def create_property_status(name):
    property_status = PropertyStatus(name=name, status=True)
    db.session.add(property_status)
    db.session.commit()
    return property_status


def update_property_status(status_id, name=None):
    ps = db.session.get(PropertyStatus, status_id)
    if not ps:
        return None
    if name is not None:
        ps.name = name
    db.session.commit()
    return ps


def delete_property_status(status_id):
    ps = db.session.get(PropertyStatus, status_id)
    if not ps:
        return None
    ps.status = False
    db.session.commit()
    return ps
