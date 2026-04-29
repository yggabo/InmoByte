from app.core.extensions import db
from sqlalchemy import func


class PropertyStatus(db.Model):
    __tablename__ = "property_status"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    status = db.Column(db.Boolean, default=True, nullable=False)
    accepts_offers = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "accepts_offers": self.accepts_offers,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<PropertyStatus {self.name}>'
