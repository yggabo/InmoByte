from flask import Blueprint
from app.api.preferences.routes import bp

preferences_bp = Blueprint('preferences', __name__)
preferences_bp.register_blueprint(bp, url_prefix='/api/preferences')

__all__ = ['preferences_bp']
