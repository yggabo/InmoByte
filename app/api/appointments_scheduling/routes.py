from flasgger import swag_from
from flask import Blueprint, request
from . import services
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from .schemas import appointment_create_schema, appointment_update_schema
from app.core.utils import success_response, error_response

bp = Blueprint('appointments', __name__)

@bp.route('', methods=['GET'])
@swag_from('docs/list_appointments.yaml')
def list_appointments():
    filters = {
        'date': request.args.get('date'),
        'client_id': request.args.get('client_id', type=int),
        'agent_id': request.args.get('agent_id', type=int),
        'property_id': request.args.get('property_id', type=int)
    }
    appointments = services.get_appointments(filters)
    return success_response(
        data=appointment_create_schema.dump(appointments, many=True),
        message="Listado de citas obtenido exitosamente"
    )

@bp.route('', methods=['POST'])
@jwt_required()
@swag_from('docs/create_appointment.yaml')
def create_appointment():
    try:
        data = appointment_create_schema.load(request.get_json())
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)
    except Exception as e:
        return error_response(f"Datos inválidos: {str(e)}", status_code=400)

    try:
        appointment = services.create_appointment(data)
        return success_response(
            data=appointment_create_schema.dump(appointment), 
            message="Cita agendada exitosamente", 
            status_code=201
        )
    except ValueError as e:
        return error_response(str(e), status_code=400)
    except Exception as e:
        if hasattr(e, 'status_code'):
            return error_response(e.message if hasattr(e, 'message') else str(e), status_code=e.status_code)
        return error_response(f"Error al crear la cita: {str(e)}", status_code=500)

@bp.route('/<int:appointment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@swag_from('docs/update_appointment.yaml')
def update_appointment(appointment_id):
    try:
        data = appointment_update_schema.load(request.get_json(), partial=True)
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)

    try:
        appointment = services.update_appointment(appointment_id, data)
        return success_response(
            data=appointment_create_schema.dump(appointment),
            message="Cita actualizada exitosamente"
        )
    except ValueError as e:
        return error_response(str(e), status_code=400)
    except Exception as e:
        if hasattr(e, 'status_code'):
            return error_response(e.message if hasattr(e, 'message') else str(e), status_code=e.status_code)
        return error_response(f"Error al actualizar la cita: {str(e)}", status_code=500)

@bp.route('/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
@swag_from('docs/delete_appointment.yaml')
def delete_appointment(appointment_id):
    try:
        services.delete_appointment(appointment_id)
        return success_response(message="Cita eliminada exitosamente")
    except Exception as e:
        # Si es una APIException la capturará el manejador global, 
        # pero si es un error de BD u otro, lo manejamos aquí.
        if hasattr(e, 'status_code'):
            raise e
        return error_response(f"Error al eliminar la cita: {str(e)}", status_code=500)
