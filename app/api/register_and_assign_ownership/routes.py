from flask import Blueprint, request, jsonify
from .services import (
    register_property, get_all_properties, get_property_by_id, 
    update_property, delete_property, assign_agent
)
from .schemas import PropertySchema

bp = Blueprint('property_api', __name__)
schema = PropertySchema()

@bp.route("/properties", methods=["POST"])
def create_property():
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    try:
        new_prop = register_property(data)
        return jsonify(schema.dump(new_prop)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/properties", methods=["GET"])
def get_properties():
    properties = get_all_properties()
    # many=True le indica al esquema que vamos a procesar una LISTA de propiedades
    return jsonify(schema.dump(properties, many=True)), 200

@bp.route("/properties/<int:property_id>", methods=["GET"])
def get_property(property_id):
    prop = get_property_by_id(property_id)
    if not prop:
        return jsonify({"error": "Propiedad no encontrada"}), 404
    return jsonify(schema.dump(prop)), 200

@bp.route("/properties/<int:property_id>", methods=["PUT"])
def edit_property(property_id):
    data = request.get_json()
    # partial=True permite que no todos los campos sean obligatorios al editar
    errors = schema.validate(data, partial=True)
    if errors:
        return jsonify({"error": "Datos inválidos", "details": errors}), 400
    
    updated_prop = update_property(property_id, data)
    if not updated_prop:
        return jsonify({"error": "Propiedad no encontrada"}), 404
    return jsonify(schema.dump(updated_prop)), 200

@bp.route("/properties/<int:property_id>", methods=["DELETE"])
def remove_property(property_id):
    if delete_property(property_id):
        return jsonify({"message": "Propiedad eliminada correctamente"}), 200
    return jsonify({"error": "Propiedad no encontrada"}), 404

@bp.route("/properties/<int:property_id>/assign-agent", methods=["PATCH"])
def assign(property_id):
    data = request.get_json()
    try:
        updated_prop = assign_agent(property_id, data.get("agent_id"))
        if not updated_prop:
            return jsonify({"error": "Propiedad no encontrada"}), 404
        return jsonify(schema.dump(updated_prop)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 409
