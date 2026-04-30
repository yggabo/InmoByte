from app.core.extensions import db
from app.api.register_and_assign_ownership.models import Property, PropertyStatus
from .models import Offer
from app.api.statusOffers.models import OfferStatus

def create_offer(data):
    property_id = data.get("property_id")
    property_obj = db.session.get(Property, property_id)
    
    if not property_obj:
        raise Exception("Propiedad no encontrada")
    
    if property_obj.status_id and property_obj.status:
        # Consultar estados de propiedad que aceptan ofertas desde BD
        available_statuses = PropertyStatus.query.filter_by(accepts_offers=True).all()
        available_status_names = [status.name for status in available_statuses]
        status_name = property_obj.status.name
        if status_name not in available_status_names:
            raise Exception("La propiedad no está disponible para recibir ofertas")
    
    # Obtener estado PENDIENTE desde offer_status (no hardcoded)
    pending_status = OfferStatus.query.filter_by(name='PENDIENTE').first()
    if not pending_status:
        raise Exception("Estado PENDIENTE no encontrado en offer_status")
    
    new_offer = Offer(
        offered_price=data.get("offered_price"),
        status_id=pending_status.id,
        property_id=property_id,
        client_id=data.get("client_id")
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

def update_offer_status(offer_id, new_status_id):
    offer = db.session.get(Offer, offer_id)
    if not offer:
        return None
    
    offer.status_id = new_status_id
    db.session.commit()
    
    # Obtener estado ACEPTADA desde offer_status (no hardcoded)
    accepted_status = OfferStatus.query.filter_by(name='ACEPTADA').first()
    if not accepted_status:
        raise Exception("Estado ACEPTADA no encontrado en offer_status")
    
    if new_status_id == accepted_status.id:
        property_obj = offer.property
        if property_obj:
            # Tipo de oferta se deduce del inmueble asociado (no campo type en Offer)
            property_type = property_obj.type
            new_property_status_name = "VENDIDA" if property_type == "COMPRA" else "ALQUILADA"
            
            status_record = PropertyStatus.query.filter_by(name=new_property_status_name).first()
            if status_record:
                property_obj.status_id = status_record.id
        
    db.session.commit()
    return offer