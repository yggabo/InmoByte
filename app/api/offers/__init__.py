from flask import Blueprint
from app.api.offers.routes import bp

offers_bp = Blueprint('offers', __name__)
offers_bp.register_blueprint(bp, url_prefix='/api/offers')

__all__ = ['offers_bp']