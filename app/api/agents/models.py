from app.core.extensions import db
from sqlalchemy import func
from sqlalchemy.orm import relationship


class Agent(db.Model):
    __tablename__ = "agents"

    id = db.Column(db.Integer, primary_key=True)
    userProfileId = db.Column(db.Integer, db.ForeignKey("user_profiles.id"), unique=True)
    status = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    userProfile = relationship("UserProfile", backref=db.backref("agent", uselist=False))

    def to_dict(self):
        return {
            "id": self.id,
            "userProfileId": self.userProfileId,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Agent {self.id}>'