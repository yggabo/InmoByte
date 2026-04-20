import os
import logging
from app.core.extensions import cors


def register_cors(app):
    """Registra y configura CORS en la aplicación."""
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000')
    origins_list = [o.strip() for o in cors_origins.split(',') if o.strip()]
    
    def origin_check(req_origin):
        if req_origin is None:
            return None
        if req_origin in origins_list:
            return req_origin
        app.logger.warning(f"Origin no permitido rechazado: {req_origin}")
        return False
    
    cors.init_app(app, 
        origins=origin_check,
        resources={
            r"/*": {
                "origins": origins_list,
                "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "max_age": 3600
            }
        },
        send_wildcard=False,
        vary_header=True
    )