import os

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///dev.db')
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test_secret_key_with_32_chars_min!'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    DEBUG = False

config_by_name = dict(
    dev=DevelopmentConfig,
    development=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)