from flask import Blueprint, request
from app.api.agents import services
from app.api.agents.schemas import agent_create_schema
from app.core.utils import success_response, error_response
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

bp = Blueprint('agents', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_all_agents():
    status_filter = request.args.get('status')
    if status_filter is not None:
        status_filter = status_filter.lower() == 'true'
    
    agents = services.get_all_agents(status_filter)
    return success_response(data=[agent.to_dict() for agent in agents])


@bp.route('/<int:agent_id>', methods=['GET'])
@jwt_required()
def get_agent(agent_id):
    agent = services.get_agent_by_id(agent_id)
    if not agent:
        return error_response("Agente no encontrado", status_code=404)
    return success_response(data=agent.to_dict())


@bp.route('', methods=['POST'])
@jwt_required()
def create_agent():
    try:
        data = agent_create_schema.load(request.get_json())
    except ValidationError as e:
        return error_response(f"Error de validación: {e.messages}", status_code=400)
    
    existing = services.get_agent_by_userProfileId(data.get('userProfileId'))
    if existing:
        return error_response("Ya existe un agente para este perfil de usuario", status_code=400)
    
    agent = services.create_agent(data.get('userProfileId'))
    return success_response(data=agent.to_dict(), message="Agente creado exitosamente", status_code=201)


@bp.route('/<int:agent_id>', methods=['DELETE'])
@jwt_required()
def delete_agent(agent_id):
    agent = services.delete_agent(agent_id)
    if not agent:
        return error_response("Agente no encontrado", status_code=404)
    
    return success_response(message="Agente eliminado exitosamente")