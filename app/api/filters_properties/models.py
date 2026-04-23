from app.core.extensions import db
from datetime import datetime, timezone

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # apartment, house, land, etc.
    location = db.Column(db.String(100), nullable=False) # zone/city
    rooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    living_space = db.Column(db.Float, nullable=True)  # Square meters
    status_id = db.Column(db.String(20), default='available') # status-ID
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'type': self.type,
            'location': self.location,
            'rooms': self.rooms,
            'bathrooms': self.bathrooms,
            'living_space': self.living_space,
            'status_id': self.status_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
