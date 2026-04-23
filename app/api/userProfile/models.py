from app.core.extensions import db
from sqlalchemy import func
from sqlalchemy.orm import relationship


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastNames = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20))
    rolId = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    role = relationship('Roles', foreign_keys=[rolId])
    user = relationship('Users', foreign_keys=[userId])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastNames": self.lastNames,
            "telefono": self.telefono,
            "rolId": self.rolId,
            "userId": self.userId,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<UserProfile {self.name} {self.lastNames}>'