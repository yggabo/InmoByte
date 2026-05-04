from flasgger import swag_from
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
@swag_from('docs/create_offer.yaml')
def create_offer_endpoint():
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
@swag_from('docs/get_property_offers.yaml')
def get_property_offers(property_id):
    offers = get_offers_by_property(property_id)
    if offers is None:
        return jsonify({"error": "Propiedad no encontrada"}), 404
    return jsonify(offer_schema.dump(offers, many=True)), 200


@bp.route('/<int:offer_id>', methods=["GET"])
@jwt_required()
@swag_from('docs/get_offer.yaml')
def get_offer_endpoint(offer_id):
    offer = get_offer_by_id(offer_id)
    if not offer:
        return jsonify({"error": "Oferta no encontrada"}), 404
    return jsonify(offer_schema.dump(offer)), 200


@bp.route('', methods=["GET"])
@jwt_required()
@swag_from('docs/get_all_offers.yaml')
def get_all_offers():
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
@swag_from('docs/update_offer_status.yaml')
def update_offer_status_endpoint(offer_id):
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