from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.api.auth.models import Users

bp = Blueprint('main', __name__)


@bp.route('/')
def hello_world():
    return render_template('main/home.html')


@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = db.session.get(Users, current_user_id)
    return jsonify(
        msg="¡Accediste a una ruta segura verificando tokens!",
        user=user.username
    )