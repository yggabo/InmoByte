from app.core.extensions import db
from datetime import datetime

class Offer(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    offered_price = db.Column(db.Numeric(12, 2))
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("offer_status.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property = db.relationship("Property", backref="offers")
    client = db.relationship("Client", backref="offers")
    status = db.relationship("OfferStatus", backref="offers")

    def to_dict(self):
        return {
            'id': self.id,
            'offered_price': float(self.offered_price) if self.offered_price else None,
            'status': self.status.name if self.status else None,
            'property_id': self.property_id,
            'client_id': self.client_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }