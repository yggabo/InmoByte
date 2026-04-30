from flasgger import swag_from
from flask import Blueprint, request
from app.api.propertyStatus import services
from app.api.propertyStatus.schemas import property_status_create_schema, property_status_update_schema
from app.core.utils import success_response, error_response
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

bp = Blueprint('propertyStatus', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
@swag_from('docs/get_all_property_statuses.yaml')
def get_all_property_statuses():
    status_filter = request.args.get('status')
    if status_filter is not None:
        status_filter = status_filter.lower() == 'true'
    statuses = services.get_all_property_statuses(status_filter)
    return success_response(data=[s.to_dict() for s in statuses])


@bp.route('/<int:status_id>', methods=['GET'])
@jwt_required()
@swag_from('docs/get_property_status.yaml')
def get_property_status(status_id):
    ps = services.get_property_status_by_id(status_id)
    if not ps:
        return error_response("Estado de propiedad no encontrado", status_code=404)
    return success_response(data=ps.to_dict())


@bp.route('', methods=['POST'])
@jwt_required()
@swag_from('docs/create_property_status.yaml')
def create_property_status():
    try:
        data = property_status_create_schema.load(request.get_json())
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)
    existing = services.get_property_status_by_name(data.get('name'))
    if existing:
        return error_response("Ya existe un estado con ese nombre", status_code=400)
    ps = services.create_property_status(data.get('name'))
    return success_response(data=ps.to_dict(), message="Estado creado exitosamente", status_code=201)


@bp.route('/<int:status_id>', methods=['PUT'])
@jwt_required()
@swag_from('docs/update_property_status.yaml')
def update_property_status(status_id):
    try:
        data = property_status_update_schema.load(request.get_json())
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)
    ps = services.update_property_status(status_id, data.get('name'))
    if not ps:
        return error_response("Estado de propiedad no encontrado", status_code=404)
    return success_response(data=ps.to_dict(), message="Estado actualizado exitosamente")


@bp.route('/<int:status_id>', methods=['DELETE'])
@jwt_required()
@swag_from('docs/delete_property_status.yaml')
def delete_property_status(status_id):
    ps = services.delete_property_status(status_id)
    if not ps:
        return error_response("Estado de propiedad no encontrado", status_code=404)
    return success_response(message="Estado eliminado exitosamente")
