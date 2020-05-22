# Application Modules

from app.classes.models.request import Status
from app.classes.controllers.utils import get_user, get_users
from app.classes.controllers.schedule_controller import ScheduleController
from app.classes.controllers.requestcontroller import SwapRequestController, UserRequestController

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

@web.route('/request/swap')
@jwt_required()
def web_get_swap_request():
    """Retrieves a specific request using swap_request_id

    Args:
        request_params: contains request_id

    Return:
        response: json response object containg request attributes
        status: success status code

    """
    response, status = jsonify(err='An Error Ocurred: Bad Request'), 400

    request_id = request.args.get('request_id')
    if request_id:
        swap_request = SwapRequestController.generate_request_dict(request_id)

        if not swap_request:
            response, status = jsonify(err='Swap Request Not found'), 404
        else:
            response, status = jsonify(swap_request), 200

    return response, status

@web.route('/request/swap', methods=['POST'])
@jwt_required()
def web_post_swap_request():
    """Creates a new swap request

    Args:
        request_param: contains reqeust_labtech_timeslot_id

    Return:
        response: message stating the outcome of attempting to create a new swap
        request
        status: success status code

    """
    response, status = jsonify(err='An Error Ocurred: Bad Request'), 400

    timeslot_id = request.get_json()['request_labtech_timeslot_id']
    labtech_id = current_identity.uwiIssuedID

    if timeslot_id:
        request_success = SwapRequestController.request_swap(labtech_id,
                                                             timeslot_id)

        if request_success:
            response, status = jsonify(message='Request made'), 201
        else:
            response, status = jsonify(message='Request could not be created'), 500
    return response, status

@web.route('/requests/swap')
@jwt_required()
def web_get_swap_requests():
    """Returns response object with all swap requests

    Args:
        None

    Return:
        response: json object containing all swap requests
        status: success status code

    """
    response, status = jsonify(err="No Swap Requests"), 200
    swap_requests = SwapRequestController.generate_all_requests()

    if swap_requests:
        response = jsonify(swap_requests)
    return response, status

@web.route('/request/swap/accept', methods=['PATCH'])
@jwt_required()
def web_accept_swap_request():
    """Allows a labtech to accept swap request made from another labtech

    Args:
        request: contains swap_request_id and confirm_timeslot_id

    Return:
        message: indicates what occured during operation
        status: success status code

    """
    response, status = jsonify(err='An Error occured: Bad Request'), 400

    swap_request_id = request.get_json()['swap_request_id']
    confirm_timeslot_id = request.get_json()['confirm_timeslot_id']

    if swap_request_id and confirm_timeslot_id:
        labtech_id = current_identity.uwiIssuedID
        update_success = SwapRequestController.accept_swap(labtech_id,
                                                           confirm_timeslot_id,
                                                          swap_request_id)

        if update_success:
            response, status = jsonify(message='Request Updated'), 200
        else:
            response, status = jsonify(message='Request could not be created'), 500
    return response, status

@web.route('/request/swap/approve', methods=['PATCH'])
@jwt_required()
def web_approve_swap_request():
    """Allows a labtech to accept swap request made from another labtech

    Args:
        request: contains swap_request_id and confirm_timeslot_id

    Return:
        message: indicates what occured during operation
        status: success status code

    """
    response, status = jsonify(err='An Error occured: Bad Request'), 400

    swap_request_id = request.get_json()['swap_request_id']
    approval_status = request.get_json()['status']

    if swap_request_id and approval_status:
        if approval_status == 'APPROVED':
            approval_status = Status.APPROVED
        else:
            approval_status = Status.DENIED

        admin_id = current_identity.uwiIssuedID
        update_success = SwapRequestController.approve_swap(admin_id,
                                                            approval_status,
                                                            swap_request_id)

        if update_success:
            response, status = jsonify(message='Request Updated'), 200
        else:
            response, status = jsonify(message='Request could not be created'), 500
    return response, status

@web.route('/request/user')
@jwt_required()
def web_get_user_request():
    """Retrieves a specific user request

    Args:
        request_params: contains request_id

    Return:
        response: json object containing a given user request

    """
    response, status = jsonify(err='An Error Ocurred: Bad Request'), 400

    request_id = request.args.get('request_id')
    if request_id:
        swap_request = UserRequestController.generate_request_dict(request_id)

        if not swap_request:
            response, status = jsonify(err='User Request Not found'), 404
        else:
            response, status = jsonify(swap_request), 200

    return response, status
