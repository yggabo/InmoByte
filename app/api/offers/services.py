from app.core.extensions import db
from app.api.register_and_assign_ownership.models import Property, PropertyStatus
from .models import Offer
from .schemas import OfferStatus, OfferTypeEnum

AVAILABLE_STATES = ["DISPONIBLE", "ASIGNADA"]

def create_offer(data):
    property_id = data.get("property_id")
    property_obj = db.session.get(Property, property_id)
    
    if not property_obj:
        raise Exception("Propiedad no encontrada")
    
    if property_obj.status_id and property_obj.status:
        status_name = property_obj.status.name
        if status_name not in AVAILABLE_STATES:
            raise Exception("La propiedad no está disponible para recibir ofertas")
    
    new_offer = Offer(
        type=data.get("type"),
        offered_price=data.get("offered_price"),
        status=OfferStatus.PENDIENTE,
        property_id=property_id,
        client_id=data.get("client_id"),
        agent_id=data.get("agent_id")
    )
    db.session.add(new_offer)
    db.session.commit()
    return new_offer

def get_offers_by_property(property_id):
    property_obj = db.session.get(Property, property_id)
    if not property_obj:
        return None
    return Offer.query.filter_by(property_id=property_id).all()

def get_offer_by_id(offer_id):
    return db.session.get(Offer, offer_id)

def update_offer_status(offer_id, new_status):
    offer = db.session.get(Offer, offer_id)
    if not offer:
        return None
    
    offer.status = new_status
    db.session.commit()
    
    if new_status == OfferStatus.ACEPTADA:
        property_obj = offer.property
        if property_obj:
            if offer.type == OfferTypeEnum.COMPRA:
                new_status_name = "VENDIDA"
            else:
                new_status_name = "ALQUILADA"
            
            status_record = PropertyStatus.query.filter_by(name=new_status_name).first()
            if status_record:
                property_obj.status_id = status_record.id
        
    db.session.commit()
    return offer