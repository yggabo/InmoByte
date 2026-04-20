from flask import Blueprint
from app.api.main.routes import bp

main_bp = Blueprint('main', __name__)
main_bp.register_blueprint(bp, url_prefix='')

__all__ = ['main_bp']