from flask import Blueprint
from app.api.agents.routes import bp

agents_bp = Blueprint('agents', __name__)
agents_bp.register_blueprint(bp, url_prefix='/api/agents')

__all__ = ['agents_bp']