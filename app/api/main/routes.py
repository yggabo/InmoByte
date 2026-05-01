from flasgger import swag_from
from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.api.auth.models import Users
from app.api.filters_properties.services import PropertyService

bp = Blueprint('main', __name__)


@bp.route('/')
@swag_from('docs/hello_world.yaml')
def hello_world():
    return render_template('main/home.html')




@bp.route('/filter-properties')
def filter_properties():
    options = PropertyService.get_filter_options()
    return render_template('main/jinja_filter.html', options=options)


@bp.route('/protected', methods=['GET'])
@jwt_required()
@swag_from('docs/protected.yaml')
def protected():
    current_user_id = get_jwt_identity()
    user = db.session.get(Users, current_user_id)
    return jsonify(
        msg="¡Accediste a una ruta segura verificando tokens!",
        user=user.username
    )