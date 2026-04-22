from flask import Blueprint
from app.api.filters-properties.routes import bp    

filters-properties_bp = Blueprint('filters-properties', __name__)
filters-properties_bp.register_blueprint(bp, url_prefix='/api/filters-properties')

__all__ = ['filters-properties_bp'] 