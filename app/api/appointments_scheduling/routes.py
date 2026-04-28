from flask import Blueprint, request
from . import services
from .schemas import appointment_create_schema
from app.core.utils import success_response, error_response
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

bp = Blueprint('appointments', __name__)

@bp.route('', methods=['POST'])
@jwt_required()
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
        return error_response(f"Error al crear la cita: {str(e)}", status_code=500)
