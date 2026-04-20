from flask import jsonify
from flask_jwt_extended import JWTManager

def register_jwt_handlers(jwt: JWTManager):
    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify({
            "message": "No autorizado - Token no proporcionado",
            "status_code": 401,
            "error": "Unauthorized"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({
            "message": "No autorizado - Token inválido",
            "status_code": 401,
            "error": "Unauthorized"
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "No autorizado - Token expirado",
            "status_code": 401,
            "error": "Unauthorized"
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "No autorizado - Token revocado",
            "status_code": 401,
            "error": "Unauthorized"
        }), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        from app.core.extensions import db
        from app.api.auth.models import TokenBlocklist
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None