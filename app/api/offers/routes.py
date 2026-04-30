from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .services import create_offer, get_offers_by_property, get_offer_by_id, update_offer_status
from .schemas import OfferSchema, OfferStatusUpdateSchema
from .models import Offer

bp = Blueprint('offers', __name__)
offer_schema = OfferSchema()
offer_status_schema = OfferStatusUpdateSchema()

@bp.route("/", methods=["POST"])
@jwt_required()
def create_offer_endpoint():
    """
    Create a new offer (purchase or rental)
    ---
    tags:
      - Offers
    summary: Create a new offer
    description: Creates a new offer for a property. The offer type (COMPRA/ALQUILER) is determined by the property.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - offered_price
            - property_id
            - client_id
          properties:
            offered_price:
              type: number
              description: Offered price amount
            property_id:
              type: integer
              description: Property ID (determines if offer is for purchase or rental)
            client_id:
              type: integer
              description: Client ID (buyer/renter)
    responses:
      201:
        description: Offer created successfully
      400:
        description: Invalid data or missing fields
      409:
        description: Property not available for offers
      500:
        description: Internal server error
    """
    data = request.get_json()
    errors = offer_schema.validate(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    try:
        new_offer = create_offer(data)
        return jsonify(offer_schema.dump(new_offer)), 201
    except Exception as e:
        error_msg = str(e)
        if "no está disponible" in error_msg.lower():
            return jsonify({"error": error_msg}), 409
        return jsonify({"error": error_msg}), 500


@bp.route("/properties/<int:property_id>/offers", methods=["GET"])
@jwt_required()
def get_property_offers(property_id):
    """
    Get all offers for a property
    ---
    tags:
      - Offers
    summary: Get property offers
    description: Retrieves all offers associated with a specific property
    parameters:
      - name: property_id
        in: path
        required: true
        schema:
          type: integer
        description: Property ID
    responses:
      200:
        description: List of offers retrieved successfully
      404:
        description: Property not found
    """
    offers = get_offers_by_property(property_id)
    if offers is None:
        return jsonify({"error": "Propiedad no encontrada"}), 404
    return jsonify(offer_schema.dump(offers, many=True)), 200


@bp.route('/<int:offer_id>', methods=["GET"])
@jwt_required()
def get_offer_endpoint(offer_id):
    """
    Get a single offer by ID
    ---
    tags:
      - Offers
    summary: Get offer details
    description: Retrieves details of a specific offer
    parameters:
      - name: offer_id
        in: path
        required: true
        schema:
          type: integer
        description: Offer ID
    responses:
      200:
        description: Offer retrieved successfully
      404:
        description: Offer not found
    """
    offer = get_offer_by_id(offer_id)
    if not offer:
        return jsonify({"error": "Oferta no encontrada"}), 404
    return jsonify(offer_schema.dump(offer)), 200


@bp.route('', methods=["GET"])
@jwt_required()
def get_all_offers():
    """
    Get all offers with optional filters
    ---
    tags:
      - Offers
    summary: List all offers
    description: Retrieves all offers, optionally filtered by property_id, client_id, or status_id
    parameters:
      - name: property_id
        in: query
        required: false
        schema:
          type: integer
        description: Filter by property ID
      - name: client_id
        in: query
        required: false
        schema:
          type: integer
        description: Filter by client ID
      - name: status_id
        in: query
        required: false
        schema:
          type: integer
        description: Filter by status ID
    responses:
      200:
        description: List of offers retrieved successfully
    """
    query = Offer.query
    
    property_id = request.args.get('property_id', type=int)
    client_id = request.args.get('client_id', type=int)
    status_id = request.args.get('status_id', type=int)
    
    if property_id:
        query = query.filter_by(property_id=property_id)
    if client_id:
        query = query.filter_by(client_id=client_id)
    if status_id:
        query = query.filter_by(status_id=status_id)
    
    offers = query.all()
    return jsonify(offer_schema.dump(offers, many=True)), 200


@bp.route('/<int:offer_id>/status', methods=["PATCH"])
@jwt_required()
def update_offer_status_endpoint(offer_id):
    """
    Update offer status
    ---
    tags:
      - Offers
    summary: Update offer status
    description: Updates the status of an offer (accept=2, reject=3, cancel=4)
    parameters:
      - name: offer_id
        in: path
        required: true
        schema:
          type: integer
        description: Offer ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - status_id
          properties:
            status_id:
              type: integer
              enum: [2, 3, 4]
              description: Status ID (2=ACEPTADA, 3=RECHAZADA, 4=CANCELADA)
    responses:
      200:
        description: Offer status updated successfully
      400:
        description: Invalid data
      404:
        description: Offer not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    errors = offer_status_schema.validate(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    offer = get_offer_by_id(offer_id)
    if not offer:
        return jsonify({"error": "Oferta no encontrada"}), 404
    
    new_status_id = data.get("status_id")
    updated_offer = update_offer_status(offer_id, new_status_id)
    if not updated_offer:
        return jsonify({"error": "Error al actualizar oferta"}), 500
    
    return jsonify(offer_schema.dump(updated_offer)), 200