from app.api.register_and_assign_ownership.models import Property

# Re-export Property from the shared register_and_assign_ownership models module.
# This makes filters_properties use the same model implementation.
__all__ = ['Property']
