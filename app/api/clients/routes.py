from flask import Blueprint, request
from app.api.clients import services
from app.api.clients.schemas import client_create_schema, client_update_schema
from app.core.utils import success_response, error_response
from app.core.exceptions import APIException
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

bp = Blueprint('clients', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_all_clients():
    clients = services.get_all_clients()
    return success_response(data=[client.to_dict() for client in clients])


@bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    client = services.get_client_by_id(client_id)
    if not client:
        return error_response("Cliente no encontrado", status_code=404)
    return success_response(data=client.to_dict())


@bp.route('', methods=['POST'])
@jwt_required()
def create_client():
    try:
        data = client_create_schema.load(request.get_json())
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)

    existing = services.get_client_by_email(data.get('email'))
    if existing:
        return error_response("El email ya existe", status_code=400)

    client = services.create_client(data)
    return success_response(data=client.to_dict(), message="Cliente creado exitosamente", status_code=201)


@bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    try:
        data = client_update_schema.load(request.get_json())
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)

    if not data:
        return error_response("No se proporcionaron datos para actualizar", status_code=400)

    client = services.update_client(client_id, data)
    if client is None:
        return error_response("Cliente no encontrado", status_code=404)
    if client is False:
        return error_response("El email ya existe", status_code=400)

    return success_response(data=client.to_dict(), message="Cliente actualizado exitosamente")


@bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    client = services.delete_client(client_id)
    if not client:
        return error_response("Cliente no encontrado", status_code=404)

    return success_response(message="Cliente eliminado exitosamente")