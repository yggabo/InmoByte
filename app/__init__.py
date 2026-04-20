import os
from flask import Flask
from dotenv import load_dotenv

from app.core.config import config_by_name
from app.core.extensions import db, jwt, bcrypt
from app.core.errors import register_error_handlers
from app.core.jwt_handlers import register_jwt_handlers
from app.core.cors_config import register_cors
from app.core.blueprints import register_blueprints
from app.core.models import register_models
from app.core.jwt_config import JWTConfig

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
    
    register_cors(app)
    register_error_handlers(app)
    register_models()
    register_blueprints(app)
    register_jwt_handlers(jwt)
    
    with app.app_context():
        db.create_all()
    
    return app