def register_models():
    """Import models explicitly so SQLAlchemy knows they exist."""
    from app.api.auth.models import Users, TokenBlocklist
    from app.api.examples_yeremi.modularization.users.models import UsersProfile