from flask import Blueprint
from app.api.filters_properties.routes import bp

filters_properties_bp = Blueprint('filters_properties_wrapper', __name__)
filters_properties_bp.register_blueprint(bp, url_prefix='/api/filter-properties')

__all__ = ['filters_properties_bp']