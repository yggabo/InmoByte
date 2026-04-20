from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({
            "message": "Bad request",
            "status_code": 400,
            "error": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "message": "Ruta no encontrada",
            "status_code": 404,
            "error": "Not Found"
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({
            "message": "Método HTTP no permitido",
            "status_code": 405,
            "error": "Method Not Allowed"
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({
            "message": "Error interno del servidor",
            "status_code": 500,
            "error": "Internal Server Error"
        }), 500

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({
                "message": str(e.description) if hasattr(e, 'description') else str(e),
                "status_code": e.code,
                "error": e.name
            }), e.code
        return jsonify({
            "message": "Error inesperado",
            "status_code": 500,
            "error": "Internal Server Error"
        }), 500

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return jsonify({
            "message": "No autorizado - Token inválido o expirado",
            "status_code": 401,
            "error": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def handle_forbidden(e):
        return jsonify({
            "message": "Origin no permitido",
            "status_code": 403,
            "error": "Forbidden"
        }), 403

    @app.errorhandler(422)
    def handle_unprocessable_entity(e):
        return jsonify({
            "message": "Entidad no procesable",
            "status_code": 422,
            "error": "Unprocessable Entity"
        }), 422
