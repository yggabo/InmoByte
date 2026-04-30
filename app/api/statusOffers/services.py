from app.core.extensions import db
from app.api.statusOffers.models import OfferStatus


def get_all_offer_statuses(status_filter=None):
    query = OfferStatus.query
    if status_filter is not None:
        query = query.filter(OfferStatus.status == status_filter)
    return query.all()


def get_offer_status_by_id(status_id):
    return OfferStatus.query.filter(OfferStatus.id == status_id).first()


def get_offer_status_by_name(name):
    return OfferStatus.query.filter(OfferStatus.name == name).first()


def create_offer_status(name):
    offer_status = OfferStatus(name=name, status=True)
    db.session.add(offer_status)
    db.session.commit()
    return offer_status


def update_offer_status(status_id, name=None):
    os = db.session.get(OfferStatus, status_id)
    if not os:
        return None
    if name is not None:
        os.name = name
    db.session.commit()
    return os


def delete_offer_status(status_id):
    os = db.session.get(OfferStatus, status_id)
    if not os:
        return None
    os.status = False
    db.session.commit()
    return os
