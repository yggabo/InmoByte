from flasgger import swag_from
from flask import Blueprint, request, jsonify
from app.api.filters_properties.services import PropertyService
from app.core.utils import success_response, error_response
from flask_jwt_extended import jwt_required

bp = Blueprint('filters_properties', __name__)

@bp.route('/', methods=['GET'], strict_slashes=False)
@swag_from('docs/get_filtered_properties.yaml')
def get_properties():
    filters = request.args.to_dict()
    try:
        properties = PropertyService.get_filtered_properties(filters)
        return success_response(
            data=[p.to_dict() for p in properties],
            message=f"Found {len(properties)} properties"
        )
    except Exception as e:
        return error_response(str(e), status_code=400)

@bp.route('/<int:property_id>', methods=['GET'], strict_slashes=False)
@swag_from('docs/get_property_detail.yaml')
def get_property(property_id):
    property_obj = PropertyService.get_property_by_id(property_id)
    if not property_obj:
        return error_response("Property not found", status_code=404)
    
    return success_response(data=property_obj.to_dict())

@bp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
@swag_from('docs/create_property_filter.yaml')
def create_property():
    data = request.get_json()
    if not data:
        return error_response("No data provided", status_code=400)
    
    # Validar campos requeridos
    required_fields = ['type', 'location', 'price_min', 'price_max', 'living_space_min', 'living_space_max', 'rooms', 'bathrooms', 'client_id', 'status_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return error_response(f"Missing required fields: {', '.join(missing_fields)}", status_code=400)
    
    try:
        new_property = PropertyService.create_property(data)
        return success_response(
            data=new_property.to_dict(),
            message="Property created successfully",
            status_code=201
        )
    except Exception as e:
        return error_response(str(e), status_code=400)