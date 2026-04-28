from app.core.extensions import db
from sqlalchemy import func
from sqlalchemy.orm import relationship


class AppointmentStatus(db.Model):
    __tablename__ = 'appointment_status'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<AppointmentStatus {self.name}>'


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    appointment_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Foreign Keys
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('appointment_status.id'), nullable=False)

    # Relationships
    client = relationship("Client", backref="appointments")
    property = relationship("Property", backref="appointments")
    agent = relationship("Agent", backref="appointments")
    status = relationship("AppointmentStatus", backref="appointments")

    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "appointment_date": self.appointment_date.isoformat() if self.appointment_date else None,
            "start_time": self.start_time.strftime('%H:%M:%S') if self.start_time else None,
            "end_time": self.end_time.strftime('%H:%M:%S') if self.end_time else None,
            "notes": self.notes,
            "is_active": self.is_active,
            "client_id": self.client_id,
            "property_id": self.property_id,
            "agent_id": self.agent_id,
            "status_id": self.status_id,
            "client": self.client.name if self.client else None,
            "property": self.property.location if self.property else None,
            "agent_id_info": self.agent_id if self.agent else None,
            "status_name": self.status.name if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date}>'
