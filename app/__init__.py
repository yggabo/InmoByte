import os
from flask import Flask
from dotenv import load_dotenv
from flasgger import Swagger

from app.core.config import config_by_name
from app.core.extensions import db, jwt, bcrypt, migrate
from app.core.errors import register_error_handlers
from app.core.jwt_handlers import register_jwt_handlers
from app.core.cors_config import register_cors
from app.core.blueprints import register_blueprints
from app.core.models import register_models
from app.core.jwt_config import JWTConfig
from app.api.roles.seeds import seed_roles
from app.api.hu_006_appointments_scheduling.seeds import seed_appointment_status

load_dotenv()


def create_app(config_name=None):
    app = Flask(__name__)
    
    if not config_name:
        config_name = os.getenv('FLASK_ENV', 'dev')
    
    app.config.from_object(config_by_name[config_name])
    
    app.config['JWT_TOKEN_LOCATION'] = JWTConfig.JWT_TOKEN_LOCATION
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWTConfig.JWT_ACCESS_TOKEN_EXPIRES
    
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    app.config['SWAGGER'] = {
        'title': 'InmoByte API',
        'uiversion': 3,
        'info': {
            'title': 'InmoByte API',
            'version': '1.0',
            'description': 'API for real estate management system'
        }
    }
    Swagger(app)

    register_cors(app)
    register_error_handlers(app)
    register_models()
    register_blueprints(app)
    register_jwt_handlers(jwt)
    
    migrations_dir = os.path.join(os.path.dirname(__file__), '..', 'migrations')
    if not os.path.exists(migrations_dir):
        with app.app_context():
            db.create_all()

    with app.app_context():
        db.create_all()
        seed_roles()
        seed_appointment_status()
    
    return app