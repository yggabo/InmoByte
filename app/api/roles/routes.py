from flasgger import swag_from
from flask import Blueprint, request
from app.api.roles import services
from app.core.utils import success_response, error_response
from app.core.exceptions import APIException
from flask_jwt_extended import jwt_required

bp = Blueprint('roles', __name__)

@bp.route('', methods=['GET'])
@swag_from('docs/get_all_roles.yaml')
def get_all_roles():
    roles = services.get_all_roles()
    return success_response(data=[role.to_dict() for role in roles])


@bp.route('/<int:role_id>', methods=['GET'])
@swag_from('docs/get_role.yaml')
def get_role(role_id):
    role = services.get_role_by_id(role_id)
    if not role:
        return error_response("Rol no encontrado", status_code=404)
    return success_response(data=role.to_dict())


@bp.route('', methods=['POST'])
@swag_from('docs/create_role.yaml')
def create_role():
    data = request.get_json()
    if not data or not data.get('name'):
        return error_response("El nombre del rol es requerido", status_code=400)

    existing = services.get_role_by_name(data['name'])
    if existing:
        return error_response("El rol ya existe", status_code=400)

    role = services.create_role(data['name'])
    return success_response(data=role.to_dict(), message="Rol creado exitosamente", status_code=201)


@bp.route('/<int:role_id>', methods=['PUT'])
@jwt_required()
@swag_from('docs/update_role.yaml')
def update_role(role_id):
    data = request.get_json()
    if not data:
        return error_response("No se proporcionaron datos para actualizar", status_code=400)

    role = services.update_role(role_id, data)
    if role is None:
        return error_response("Rol no encontrado", status_code=404)
    if role is False:
        return error_response("El nombre del rol ya existe", status_code=400)

    return success_response(data=role.to_dict(), message="Rol actualizado exitosamente")


@bp.route('/<int:role_id>', methods=['DELETE'])
@jwt_required()
@swag_from('docs/delete_role.yaml')
def delete_role(role_id):
    role = services.delete_role(role_id)
    if not role:
        return error_response("Rol no encontrado", status_code=404)

    return success_response(message="Rol eliminado exitosamente")