from flasgger import swag_from
from flask import Blueprint, request
from app.api.userProfile import services
from app.api.userProfile.schemas import (
    user_profile_schema,
    user_profiles_schema,
    user_profile_update_schema
)
from app.core.utils import success_response, error_response
from flask_jwt_extended import jwt_required

bp = Blueprint('userProfile', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
@swag_from('docs/get_all_user_profiles.yaml')
def get_all_user_profiles():
    profiles = services.get_all_user_profiles()
    return success_response(data=[profile.to_dict() for profile in profiles])


@bp.route('/<int:profile_id>', methods=['GET'])
@jwt_required()
@swag_from('docs/get_user_profile.yaml')
def get_user_profile(profile_id):
    profile = services.get_user_profile_by_id(profile_id)
    if not profile:
        return error_response("Perfil no encontrado", status_code=404)
    return success_response(data=profile.to_dict())


@bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
@swag_from('docs/get_user_profile_by_user.yaml')
def get_user_profile_by_user(user_id):
    profile = services.get_user_profile_by_user_id(user_id)
    if not profile:
        return error_response("Perfil no encontrado para este usuario", status_code=404)
    return success_response(data=profile.to_dict())


@bp.route('', methods=['POST'])
@jwt_required()
@swag_from('docs/create_user_profile.yaml')
def create_user_profile():
    data = request.get_json()
    if not data:
        return error_response("No se proporcionaron datos", status_code=400)

    errors = user_profile_schema.validate(data)
    if errors:
        return error_response("Datos inválidos", status_code=400, errors=errors)

    profile = services.create_user_profile(data)
    if profile is None:
        return error_response("Datos requeridos faltantes o usuario/rol no encontrado", status_code=400)
    if profile is False:
        return error_response("El perfil para este usuario ya existe", status_code=400)

    return success_response(data=profile.to_dict(), message="Perfil creado exitosamente", status_code=201)


@bp.route('/<int:profile_id>', methods=['PUT'])
@jwt_required()
@swag_from('docs/update_user_profile.yaml')
def update_user_profile(profile_id):
    data = request.get_json()
    if not data:
        return error_response("No se proporcionaron datos para actualizar", status_code=400)

    errors = user_profile_update_schema.validate(data)
    if errors:
        return error_response("Datos inválidos", status_code=400, errors=errors)

    profile = services.update_user_profile(profile_id, data)
    if profile is None:
        return error_response("Perfil no encontrado", status_code=404)
    if profile is False:
        return error_response("El rol no existe", status_code=400)

    return success_response(data=profile.to_dict(), message="Perfil actualizado exitosamente")


@bp.route('/<int:profile_id>', methods=['DELETE'])
@jwt_required()
@swag_from('docs/delete_user_profile.yaml')
def delete_user_profile(profile_id):
    profile = services.delete_user_profile(profile_id)
    if not profile:
        return error_response("Perfil no encontrado", status_code=404)

    return success_response(message="Perfil eliminado exitosamente")