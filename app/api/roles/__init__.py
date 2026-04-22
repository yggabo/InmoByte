from flask import Blueprint
from app.api.roles.routes import bp

roles_bp = Blueprint('roles', __name__)
roles_bp.register_blueprint(bp, url_prefix='/api/roles')

__all__ = ['roles_bp']