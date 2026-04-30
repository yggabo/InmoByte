from app.core.extensions import db
from .models import Property
from app.api.propertyStatus.models import PropertyStatus

def register_property(data):
    new_property = Property(
        type=data.get("type"),
        location=data.get("location"),
        price_min=data.get("price_min"),
        price_max=data.get("price_max"),
        living_space=data.get("living_space"),
        rooms=data.get("rooms"),
        bathrooms=data.get("bathrooms"),
        description=data.get("description"),
        client_id=data.get("client_id"),
        status_id=data.get("status_id"),
        agent_id=data.get("agent_id")
    )
    db.session.add(new_property)
    db.session.commit()
    return new_property

def get_all_properties():
    return Property.query.all()

def get_property_by_id(property_id):
    return db.session.get(Property, property_id)

def update_property(property_id, data):
    property_obj = db.session.get(Property, property_id)
    if not property_obj:
        return None
    
    # update campos dinamicamente
    for key, value in data.items():
        if hasattr(property_obj, key):
            setattr(property_obj, key, value)
    
    db.session.commit()
    return property_obj

def delete_property(property_id):
    property_obj = db.session.get(Property, property_id)
    if property_obj:
        db.session.delete(property_obj)
        db.session.commit()
        return True
    return False

def assign_agent(property_id, agent_id):
    property_obj = db.session.get(Property, property_id)
    if not property_obj:
        return None
    
    property_obj.agent_id = agent_id
    db.session.commit()
    return property_obj