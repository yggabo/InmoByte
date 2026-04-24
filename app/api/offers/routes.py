from flask import Blueprint, request, jsonify
from .services import create_offer, get_offers_by_property, get_offer_by_id, update_offer_status
from .schemas import OfferSchema, OfferStatusUpdateSchema

offers_bp = Blueprint('offers', __name__)
offer_schema = OfferSchema()
offer_status_schema = OfferStatusUpdateSchema()


@offers_bp.route("/offers", methods=["POST"])
def create_offer_endpoint():
    """
    Create a new offer (purchase or rental)
    ---
    tags:
      - Offers
    summary: Create a new offer
    description: Creates a new offer for a property (purchase or rental)
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - type
            - offered_price
            - property_id
            - client_id
          properties:
            type:
              type: string
              enum: [COMPRA, ALQUILER]
              description: Offer type (purchase or rental)
            offered_price:
              type: number
              description: Offered price amount
            property_id:
              type: integer
              description: Property ID
            client_id:
              type: integer
              description: Client ID (buyer/renter)
            agent_id:
              type: integer
              description: Agent ID (optional)
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


@offers_bp.route("/properties/<int:property_id>/offers", methods=["GET"])
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


@offers_bp.route("/offers/<int:offer_id>/status", methods=["PATCH"])
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