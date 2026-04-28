from flask import Blueprint
from app.api.clients.routes import bp

clients_bp = Blueprint('clients', __name__)
clients_bp.register_blueprint(bp, url_prefix='/api/clients')

__all__ = ['clients_bp']