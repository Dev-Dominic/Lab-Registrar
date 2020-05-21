# Application Modules

from app.classes.controllers.utils import get_user, get_users
from app.classes.controllers.schedule_controller import ScheduleController

# Flask Modules

from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

web = Blueprint('web', __name__)

@web.route('/user', methods=["GET"])
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

    user_id = request.args.get('uwiIssuedID')
    if user_id:
        response = get_user(current_identity.uwiIssuedID, user_id)
        status = 200
    else:
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

@web.route('/schedule',methods=["GET"])
@jwt_required()
def web_labtech_schedule():
    """Retrieves all users

    Args:
        request_json: contains necessary 

    Return:
        response: json object containing all related timeslots 
        status: indicating request success

    """
    response, status = jsonify({}), 400

    labtech_id = request.args.get('uwiIssuedID') 
    if labtech_id:
        schedule = ScheduleController.generate_schedule(current_identity.uwiIssuedID, labtech_id)    

        if schedule:
            response, status = jsonify(schedule), 200
    return response, status 

@web.route('/schedule/register/', methods=['PATCH'])
@jwt_required()
def web_schedule_register():
    """Registers a labtech to a given timeslot

    Args:
        request_json: contains timeslot identifier

    Return:
        response: message indicating whether the operation was a success
        status: success status code

    """
    response, status = jsonify(err='Request Invalid'), 400
    
    timeslot_id = request.get_json()['timeslot_id']
    if timeslot_id:
        # Extracting labtech_id and timeslot_id and then attempt to establish a
        # relationship with both instances

        current_id = current_identity.uwiIssuedID
        result = ScheduleController.schedule_register(current_id, timeslot_id)
        response, status  = jsonify(result), 200

    return response, status
