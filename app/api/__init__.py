from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.api.auth import auth_bp
from app.api.main import main_bp

api_bp.register_blueprint(main_bp)
api_bp.register_blueprint(auth_bp)
