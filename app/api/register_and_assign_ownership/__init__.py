from flask import Blueprint
from app.api.register_and_assign_ownership.routes import bp

register_and_assign_ownership_bp = Blueprint('register_and_assign_ownership', __name__)
register_and_assign_ownership_bp.register_blueprint(bp, url_prefix='/register_and_assign_ownership')

__all__ = ['register_and_assign_ownership_bp']