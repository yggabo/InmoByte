from flask import Blueprint

preferences_bp = Blueprint('preferences', __name__)

from app.api.preferences import routes