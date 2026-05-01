from flasgger import swag_from
from flask import Blueprint, request
from app.api.preferences.services import PreferenceService
from app.core.utils import success_response, error_response
from app.core.exceptions import APIException
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('preferences', __name__)


@bp.route('/', methods=['POST'])
@jwt_required()
@swag_from('docs/create_preference.yaml')
def create_preference():
    data = request.get_json()

    if not data:
        return error_response("No data provided", status_code=400)

    required_fields = ['client_id', 'property_type_id', 'price_min', 'price_max', 'location',
                      'bedrooms', 'bathrooms', 'additional_features',
                      'living_space_min', 'living_space_max']

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return error_response(f"Missing fields: {', '.join(missing_fields)}", status_code=400)

    client_id = data.get('client_id')

    try:
        preference = PreferenceService.create_preference(client_id, data)
        return success_response(data=preference.to_dict(), message="Preferences created successfully", status_code=201)
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)


@bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
@swag_from('docs/get_preference.yaml')
def get_preference(client_id):
    try:
        preference = PreferenceService.get_preference_by_client(client_id)
        return success_response(data=preference.to_dict())
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)


@bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
@swag_from('docs/update_preference.yaml')
def update_preference(client_id):
    data = request.get_json()

    if not data:
        return error_response("No data provided", status_code=400)

    try:
        preference = PreferenceService.update_preference(client_id, data)
        return success_response(data=preference.to_dict(), message="Preferences updated successfully")
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)
