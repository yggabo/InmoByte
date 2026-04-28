from app.core.extensions import db


class PropertyStatus(db.Model):
    __tablename__ = "property_status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    location = db.Column(db.String(255))
    price_min = db.Column(db.Numeric(12, 2))
    price_max = db.Column(db.Numeric(12, 2))
    living_space_min = db.Column(db.Numeric(10, 2))
    living_space_max = db.Column(db.Numeric(10, 2))
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
            'living_space_min': float(self.living_space_min) if self.living_space_min else None,
            'living_space_max': float(self.living_space_max) if self.living_space_max else None,
            'rooms': self.rooms,
            'bathrooms': self.bathrooms,
            'description': self.description,
            'client_id': self.client_id,
            'agent_id': self.agent_id,
            'status_id': self.status_id
        }