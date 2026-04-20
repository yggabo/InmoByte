from flask import Blueprint
from app.api.auth.routes import bp

auth_bp = Blueprint('auth', __name__)
auth_bp.register_blueprint(bp, url_prefix='/api/auth')

__all__ = ['auth_bp']