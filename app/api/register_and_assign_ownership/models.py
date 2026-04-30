from app.core.extensions import db
from app.api.propertyStatus.models import PropertyStatus


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    location = db.Column(db.String(255))
    price_min = db.Column(db.Numeric(12, 2))
    price_max = db.Column(db.Numeric(12, 2))
    living_space = db.Column(db.Numeric(10, 2))
    rooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    description = db.Column(db.String(255))

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    agent_id = db.Column(db.Integer, db.ForeignKey("agents.id"), nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey("property_status.id"))

    client = db.relationship("Client", backref="properties")
    agent = db.relationship("Agent", backref="properties")
    status = db.relationship("PropertyStatus", backref="properties")

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'location': self.location,
            'price_min': float(self.price_min) if self.price_min else None,
            'price_max': float(self.price_max) if self.price_max else None,
            'living_space': float(self.living_space) if self.living_space else None,
            'rooms': self.rooms,
            'bathrooms': self.bathrooms,
            'description': self.description,
            'client': self.client.to_dict() if self.client else None,
            'status': self.status.to_dict() if self.status else None,
            'agent': self.agent.to_dict() if self.agent else None
        }