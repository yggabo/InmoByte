from app.core.extensions import db
from datetime import datetime

class OfferStatus(db.Model):
    __tablename__ = "offer_status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

class OfferType(db.Model):
    __tablename__ = "offer_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

class Offer(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    offered_price = db.Column(db.Numeric(12, 2))
    status = db.Column(db.String(50))

    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    agent_id = db.Column(db.Integer, db.ForeignKey("agents.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property = db.relationship("Property", backref="offers")
    client = db.relationship("Client", backref="offers")
    agent = db.relationship("Agent", backref="offers")

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'offered_price': float(self.offered_price) if self.offered_price else None,
            'status': self.status,
            'property_id': self.property_id,
            'client_id': self.client_id,
            'agent_id': self.agent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }