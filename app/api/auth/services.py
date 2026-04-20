from app.api.auth.models import Users, TokenBlocklist
from app.core.extensions import db, bcrypt
from app.core.exceptions import APIException
from datetime import datetime, timezone
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
            raise APIException("User already exists", status_code=400)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Users(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def verify_credentials(username, password):
        user = Users.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None
        
    @staticmethod
    def generate_tokens(user_id):
        access_token = create_access_token(identity=str(user_id))
        refresh_token = create_refresh_token(identity=str(user_id))
        return access_token, refresh_token

    @staticmethod
    def revoke_token(jti):
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        # Explicito: si hay varias operaciones, el commit() se hace despues o aquí, dependiendo del flujo.
        db.session.commit()
