from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    response = {"message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message="Error", status_code=400, errors=None):
    response = {"message": message}
    if errors is not None:
        response["errors"] = errors
    return jsonify(response), status_code
