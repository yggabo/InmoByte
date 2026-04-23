def register_models():
    """Import models explicitly so SQLAlchemy knows they exist."""
    from app.api.auth.models import Users, TokenBlocklist
    from app.api.filters_properties.models import Property