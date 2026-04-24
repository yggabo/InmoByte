from flask import Blueprint, request
from app.api.preferences.services import PreferenceService
from app.core.utils import success_response, error_response
from app.core.exceptions import APIException
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.preferences import preferences_bp as bp


@bp.route('/clients/<int:client_id>/preferences', methods=['POST'])
@jwt_required()
def create_preference(client_id):
    """
    Create preferences for a client
    ---
    tags:
      - Preferences
    summary: Create client preferences
    description: Creates preferences for a specific client
    parameters:
      - name: client_id
        in: path
        required: true
        schema:
          type: integer
        description: Client ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - property_type_id
            - price_min
            - price_max
            - location
            - bedrooms
            - bathrooms
            - additional_features
            - living_space_min
            - living_space_max
          properties:
            property_type_id:
              type: integer
              description: Property type ID (FK to property_types table)
            price_min:
              type: number
              description: Minimum price
            price_max:
              type: number
              description: Maximum price
            location:
              type: string
              description: Preferred location
            bedrooms:
              type: integer
              description: Number of bedrooms
            bathrooms:
              type: integer
              description: Number of bathrooms
            additional_features:
              type: object
              description: Additional features as JSON
            living_space_min:
              type: number
              description: Minimum living space in m²
            living_space_max:
              type: number
              description: Maximum living space in m²
    responses:
      201:
        description: Preferences created successfully
      400:
        description: Missing required fields or invalid data
      409:
        description: Preferences already exist for this client
    security:
      - JWT: []
    """
    data = request.get_json()

    if not data:
        return error_response("No data provided", status_code=400)

    required_fields = ['property_type_id', 'price_min', 'price_max', 'location',
                      'bedrooms', 'bathrooms', 'additional_features',
                      'living_space_min', 'living_space_max']

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return error_response(f"Missing fields: {', '.join(missing_fields)}", status_code=400)

    try:
        preference = PreferenceService.create_preference(client_id, data)
        return success_response(data=preference.to_dict(), message="Preferences created successfully", status_code=201)
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)


@bp.route('/clients/<int:client_id>/preferences', methods=['GET'])
@jwt_required()
def get_preference(client_id):
    """
    Get preferences for a client
    ---
    tags:
      - Preferences
    summary: Get client preferences
    description: Retrieves preferences for a specific client
    parameters:
      - name: client_id
        in: path
        required: true
        schema:
          type: integer
        description: Client ID
    responses:
      200:
        description: Preferences retrieved successfully
      404:
        description: Preferences not found
    security:
      - JWT: []
    """
    try:
        preference = PreferenceService.get_preference_by_client(client_id)
        return success_response(data=preference.to_dict())
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)


@bp.route('/clients/<int:client_id>/preferences', methods=['PUT'])
@jwt_required()
def update_preference(client_id):
    """
    Update preferences for a client
    ---
    tags:
      - Preferences
    summary: Update client preferences
    description: Updates preferences for a specific client
    parameters:
      - name: client_id
        in: path
        required: true
        schema:
          type: integer
        description: Client ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            property_type_id:
              type: integer
              description: Property type ID
            price_min:
              type: number
              description: Minimum price
            price_max:
              type: number
              description: Maximum price
            location:
              type: string
              description: Preferred location
            bedrooms:
              type: integer
              description: Number of bedrooms
            bathrooms:
              type: integer
              description: Number of bathrooms
            additional_features:
              type: object
              description: Additional features as JSON
            living_space_min:
              type: number
              description: Minimum living space in m²
            living_space_max:
              type: number
              description: Maximum living space in m²
    responses:
      200:
        description: Preferences updated successfully
      400:
        description: No data provided
      404:
        description: Preferences not found
    security:
      - JWT: []
    """
    data = request.get_json()

    if not data:
        return error_response("No data provided", status_code=400)

    try:
        preference = PreferenceService.update_preference(client_id, data)
        return success_response(data=preference.to_dict(), message="Preferences updated successfully")
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)