from app.core.extensions import db
from app.api.hu_006_appointments_scheduling.models import AppointmentStatus

def seed_appointment_status():
    statuses_data = [
        {'name': 'PROGRAMADA', 'description': 'La cita ha sido programada y está pendiente de realización.'},
        {'name': 'REALIZADA', 'description': 'La cita se llevó a cabo exitosamente.'},
        {'name': 'CANCELADA', 'description': 'La cita fue cancelada por el cliente o el agente.'},
        {'name': 'REPROGRAMADA', 'description': 'La cita original fue movida a una nueva fecha/hora.'},
        {'name': 'NOSHOW', 'description': 'El cliente no se presentó a la cita sin previo aviso.'}
    ]

    for data in statuses_data:
        existing = AppointmentStatus.query.filter_by(name=data['name']).first()
        if not existing:
            status = AppointmentStatus(
                name=data['name'],
                description=data['description'],
                status=True
            )
            db.session.add(status)
    
    db.session.commit()
