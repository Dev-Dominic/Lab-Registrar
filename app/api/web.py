# Application Modules

from app.classes.controllers.utils import get_user

# Flask Modules

from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

web = Blueprint('web', __name__)

@web.route('/user')
@jwt_required()
def web_get_user():
    """Retrieves a filtered user data 

    Args:
        json: contains necessary data to retrieve user

    Return:
        response: object containing retrieve user data
        status: indicating request success

    """
    response, status = jsonify({}), 400

    request_keys = [key for key in request.get_json().keys()] 
    if  request_keys == ['uwiIssuedID', 'request_list']:
        try:
            user_id, request_list = request.get_json().values()
            response = get_user(current_identity.uwiIssuedID, user_id, request_list)
            status = 200

        except:
            response = jsonify(server_error='Credentials Error')

    return response, status
