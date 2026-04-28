from app.core.extensions import db
from app.api.appointments_scheduling.models import Appointment, AppointmentStatus
from app.api.register_and_assign_ownership.models import Property
from app.api.clients.models import Client
from app.api.agents.models import Agent
from datetime import datetime
from app.core.exceptions import APIException
from sqlalchemy import and_, or_

def check_scheduling_conflict(agent_id, appointment_date, start_time, end_time, exclude_id=None):
    """
    Verifica si un agente tiene conflictos de horario en una fecha específica.
    El traslape ocurre si: (Nueva_Inicio < Existente_Fin) Y (Existente_Inicio < Nueva_Fin)
    """
    query = Appointment.query.filter(
        Appointment.agent_id == agent_id,
        Appointment.appointment_date == appointment_date,
        Appointment.is_active == True,
        # Lógica de traslape
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    )

    if exclude_id:
        query = query.filter(Appointment.id != exclude_id)

    return query.first()

def get_appointments(filters=None):
    """
    Obtiene el listado de citas con filtros opcionales.
    """
    query = Appointment.query.filter(Appointment.is_active == True)

    if filters:
        if filters.get('date'):
            try:
                date_val = datetime.strptime(filters['date'], '%Y-%m-%d').date()
                query = query.filter(Appointment.appointment_date == date_val)
            except (ValueError, TypeError):
                # Si la fecha es inválida, podríamos ignorar el filtro o lanzar error.
                # Por ahora lo ignoramos para no romper el listado.
                pass
        if filters.get('client_id'):
            query = query.filter(Appointment.client_id == filters['client_id'])
        if filters.get('agent_id'):
            query = query.filter(Appointment.agent_id == filters['agent_id'])
        if filters.get('property_id'):
            query = query.filter(Appointment.property_id == filters['property_id'])

    return query.order_by(Appointment.appointment_date.asc(), Appointment.start_time.asc()).all()

def update_appointment(appointment_id, data):
    """
    Actualiza una cita existente. Valida conflictos si cambia el horario.
    """
    appointment = db.session.get(Appointment, appointment_id)
    if not appointment or not appointment.is_active:
        raise APIException("Cita no encontrada.", status_code=404)

    # Si se actualiza el horario, validar conflictos
    new_date = data.get('appointment_date', appointment.appointment_date)
    new_start = data.get('start_time', appointment.start_time)
    new_end = data.get('end_time', appointment.end_time)
    new_agent = data.get('agent_id', appointment.agent_id)

    if any(k in data for k in ['appointment_date', 'start_time', 'end_time', 'agent_id']):
        conflict = check_scheduling_conflict(
            agent_id=new_agent,
            appointment_date=new_date,
            start_time=new_start,
            end_time=new_end,
            exclude_id=appointment_id
        )
        if conflict:
            raise APIException(
                f"Conflicto de horario: El agente ya tiene una cita ({conflict.start_time} - {conflict.end_time}).",
                status_code=409
            )

    # Actualizar campos
    for key, value in data.items():
        if hasattr(appointment, key) and value is not None:
            setattr(appointment, key, value)

    db.session.commit()
    return appointment

def delete_appointment(appointment_id):
    """
    Realiza un borrado lógico de la cita.
    """
    appointment = db.session.get(Appointment, appointment_id)
    if not appointment or not appointment.is_active:
        raise APIException("Cita no encontrada o ya eliminada.", status_code=404)

    appointment.is_active = False
    db.session.commit()
    return True

def create_appointment(data):
    # 1. Validar existencia de cliente
    client = db.session.get(Client, data.get('client_id'))
    if not client:
        raise ValueError("El cliente especificado no existe.")

    # 2. Validar existencia de propiedad y estado
    property_obj = db.session.get(Property, data.get('property_id'))
    if not property_obj:
        raise ValueError("La propiedad especificada no existe.")
    
    # Validar estado de la propiedad (DISPONIBLE o ASIGNADA)
    # Asumimos que status 1 = DISPONIBLE, 2 = ASIGNADA como se ve en otros servicios
    if property_obj.status_id not in [1, 2]:
        raise ValueError("La propiedad no está disponible para agendar citas.")

    # 3. Validar existencia de agente o asignar el responsable de la propiedad
    agent_id = data.get('agent_id')
    if not agent_id:
        if not property_obj.agent_id:
            raise ValueError("La propiedad no tiene un agente asignado responsable.")
        agent_id = property_obj.agent_id
    else:
        agent = db.session.get(Agent, agent_id)
        if not agent:
            raise ValueError("El agente especificado no existe.")

    # 4. Validar conflictos de horario (HU-006-04)
    conflict = check_scheduling_conflict(
        agent_id=agent_id,
        appointment_date=data.get('appointment_date'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time')
    )
    if conflict:
        raise APIException(
            f"El agente ya tiene una cita programada en ese horario ({conflict.start_time} - {conflict.end_time}).",
            status_code=409
        )

    # 5. Determinar estado inicial (PROGRAMADA por defecto si no se envía)
    status_id = data.get('status_id')
    if not status_id:
        status_prog = AppointmentStatus.query.filter_by(name='PROGRAMADA').first()
        if status_prog:
            status_id = status_prog.id
        else:
            raise ValueError("Estado 'PROGRAMADA' no encontrado en el sistema.")
    else:
        status_obj = db.session.get(AppointmentStatus, status_id)
        if not status_obj:
            raise ValueError("El estado de cita especificado no existe.")

    # 5. Crear la cita
    new_appointment = Appointment(
        appointment_date=data.get('appointment_date'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        notes=data.get('notes'),
        client_id=data.get('client_id'),
        property_id=data.get('property_id'),
        agent_id=agent_id,
        status_id=status_id,
        is_active=True
    )

    db.session.add(new_appointment)
    db.session.commit()
    
    return new_appointment

def get_appointment_by_id(appointment_id):
    return Appointment.query.filter_by(id=appointment_id, is_active=True).first()
