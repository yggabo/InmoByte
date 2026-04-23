def register_models():
    """Import models explicitly so SQLAlchemy knows they exist."""
    from app.api.auth.models import Users, TokenBlocklist
    from app.api.roles.models import Roles
    from app.api.userProfile.models import UserProfile