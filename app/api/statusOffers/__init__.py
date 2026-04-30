from flask import Blueprint
from app.api.statusOffers.routes import bp

status_offers_bp = Blueprint('status_offers', __name__)
status_offers_bp.register_blueprint(bp, url_prefix='/api/status-offers')

__all__ = ['status_offers_bp']