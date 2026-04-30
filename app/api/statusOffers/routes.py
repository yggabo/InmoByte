from flask import Blueprint, request
from app.api.statusOffers import services
from app.api.statusOffers.schemas import offer_status_create_schema, offer_status_update_schema
from app.core.utils import success_response, error_response
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError


bp = Blueprint('statusOffers', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_all_offer_statuses():
    status_filter = request.args.get('status')
    if status_filter is not None:
        status_filter = status_filter.lower() == 'true'
    statuses = services.get_all_offer_statuses(status_filter)
    return success_response(data=[s.to_dict() for s in statuses])


@bp.route('/<int:status_id>', methods=['GET'])
@jwt_required()
def get_offer_status(status_id):
    os = services.get_offer_status_by_id(status_id)
    if not os:
        return error_response("Estado de oferta no encontrado", status_code=404)
    return success_response(data=os.to_dict())


@bp.route('', methods=['POST'])
@jwt_required()
def create_offer_status():
    try:
        data = offer_status_create_schema.load(request.get_json())
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)
    existing = services.get_offer_status_by_name(data.get('name'))
    if existing:
        return error_response("Ya existe un estado con ese nombre", status_code=400)
    os = services.create_offer_status(data.get('name'))
    return success_response(data=os.to_dict(), message="Estado creado exitosamente", status_code=201)


@bp.route('/<int:status_id>', methods=['PUT'])
@jwt_required()
def update_offer_status(status_id):
    try:
        data = offer_status_update_schema.load(request.get_json())
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)
    os = services.update_offer_status(status_id, data.get('name'))
    if not os:
        return error_response("Estado de oferta no encontrado", status_code=404)
    return success_response(data=os.to_dict(), message="Estado actualizado exitosamente")


@bp.route('/<int:status_id>', methods=['DELETE'])
@jwt_required()
def delete_offer_status(status_id):
    os = services.delete_offer_status(status_id)
    if not os:
        return error_response("Estado de oferta no encontrado", status_code=404)
    return success_response(message="Estado eliminado exitosamente")
