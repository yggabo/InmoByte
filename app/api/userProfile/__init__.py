from flask import Blueprint
from app.api.userProfile.routes import bp

userProfile_bp = Blueprint('userProfile', __name__)
userProfile_bp.register_blueprint(bp, url_prefix='/api/user-profile')

__all__ = ['userProfile_bp']