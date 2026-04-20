from flask import Blueprint, request
from datetime import datetime, timezone, timedelta
from app.api.auth.services import AuthService
from app.core.utils import success_response, error_response
from app.core.exceptions import APIException
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
    create_access_token,
    create_refresh_token
)

# Blueprint prefix will be handled on register in app.__init__.py
bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return error_response("Missing field", status_code=400)

    try:
        AuthService.register_user(data['username'], data['email'], data['password'])
        return success_response(message="Usuario registrado exitosamente", status_code=201)
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return error_response("Faltan credenciales", status_code=400)

    user = AuthService.verify_credentials(data['username'], data['password'])
    
    if user:
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        resp, code = success_response(
            data={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_in': 3600,
                'login': True
            },
            message="Login exitoso"
        )
        return resp, code

    return error_response("Credenciales inválidas", status_code=401)

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    AuthService.revoke_token(jti)
    
    return success_response(message="Logout exitoso")

@bp.route('/keep-alive', methods=['POST'])
@jwt_required()
def keep_alive():
    jwt_data = get_jwt()
    exp_timestamp = jwt_data["exp"]
    current_timestamp = datetime.now(timezone.utc).timestamp()
    seconds_remaining = exp_timestamp - current_timestamp
    
    response_data = {
        "valid": True,
        "expires_in": int(seconds_remaining),
        "new_token": None
    }
    
    if seconds_remaining < 300:
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id)
        response_data["new_token"] = new_token
        response_data["expires_in"] = 3600
        response_data["renewed"] = True
    else:
        response_data["renewed"] = False
    
    return success_response(data=response_data)
