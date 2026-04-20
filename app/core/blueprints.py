def register_blueprints(app):
    """Register all application blueprints."""
    from app.api import api_bp
    app.register_blueprint(api_bp)