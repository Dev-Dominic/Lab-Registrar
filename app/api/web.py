# Application Modules

from app.classes.controllers.utils import get_user, get_users

# Flask Modules

from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

web = Blueprint('web', __name__)

@web.route('/user')
@jwt_required()
def web_get_user():
    """Retrieves a filtered user data 

    Args:
        request_json: contains necessary data to retrieve user

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

@web.route('/users')
@jwt_required()
def web_get_users():
    """Retrieves all users

    Args:
        request_json: contains necessary 

    Return:
        response: json object containing all users
        status: indicating request success

    """
    response, status = jsonify({}), 403

    # Checks that users were retrieve, because get_users checks that admins are
    # making the request and will generate empty dictionary otherwise

    users = get_users(current_identity.uwiIssuedID) 
    if users:
        response, status = jsonify(users), 200

    return response, status
