from flask import Blueprint
from app.api.appointments_scheduling.routes import bp

appointments_scheduling_bp = Blueprint('appointments_scheduling', __name__)
appointments_scheduling_bp.register_blueprint(bp, url_prefix='/api/appointments')

__all__ = ['appointments_scheduling_bp']
