from flask import Blueprint
from app.api.propertyStatus.routes import bp

propertyStatus_bp = Blueprint('propertyStatus', __name__)
propertyStatus_bp.register_blueprint(bp, url_prefix='/api/property-status')

__all__ = ['propertyStatus_bp']
