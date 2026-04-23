from flask import Blueprint, request, jsonify
from app.api.filters_properties.services import PropertyService
from app.core.utils import success_response, error_response
from flask_jwt_extended import jwt_required

bp = Blueprint('filters_properties', __name__)

@bp.route('/', methods=['GET'])
def get_properties():
    """
    Endpoint to search properties with filters.
    Matches HU-004 requirements.
    Usage: GET /api/properties?type=house&location=Madrid
    """
    filters = request.args.to_dict()
    try:
        properties = PropertyService.get_filtered_properties(filters)
        return success_response(
            data=[p.to_dict() for p in properties],
            message=f"Found {len(properties)} properties"
        )
    except Exception as e:
        return error_response(str(e), status_code=400)

@bp.route('/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """
    Endpoint to get a single property details.
    """
    property_obj = PropertyService.get_property_by_id(property_id)
    if not property_obj:
        return error_response("Property not found", status_code=404)
    
    return success_response(data=property_obj.to_dict())

@bp.route('/', methods=['POST'])
@jwt_required()
def create_property():
    """
    Endpoint to create a new property. Requires authentication.
    """
    data = request.get_json()
    if not data:
        return error_response("No data provided", status_code=400)
    
    try:
        new_property = PropertyService.create_property(data)
        return success_response(
            data=new_property.to_dict(),
            message="Property created successfully",
            status_code=201
        )
    except Exception as e:
        return error_response(str(e), status_code=400)
