from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.api.auth import auth_bp
from app.api.main import main_bp
from app.api.filters_properties import filters_properties_bp
from app.api.register_and_assign_ownership import register_and_assign_ownership_bp

api_bp.register_blueprint(main_bp)
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(filters_properties_bp)
api_bp.register_blueprint(register_and_assign_ownership_bp)
