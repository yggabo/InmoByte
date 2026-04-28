from app.core.extensions import db
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy import func


class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    property_type_id = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    bedrooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    additional_features = db.Column(JSON, nullable=True)
    living_space_min = db.Column(db.Float, nullable=True)
    living_space_max = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "property_type_id": self.property_type_id,
            "price": self.price,
            "location": self.location,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "additional_features": self.additional_features,
            "living_space_min": self.living_space_min,
            "living_space_max": self.living_space_max,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Preference client_id={self.client_id}>'