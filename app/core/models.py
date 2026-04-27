def register_models():
    """Import models explicitly so SQLAlchemy knows they exist."""
    from app.api.auth.models import Users, TokenBlocklist
    from app.api.roles.models import Roles
    from app.api.userProfile.models import UserProfile
    from app.api.preferences.models import Preference
    from app.api.register_and_assign_ownership.models import Property
    from app.api.clients.models import Client
    from app.api.agents.models import Agent
