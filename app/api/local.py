# Application Modules

from app.classes.controllers.access_controller import AccessController

# Flask Modules

from flask import Blueprint, jsonify, request

local = Blueprint('local', __name__) 

@local.route('/clockin', methods=['POST'])
def clock_in(): 
    """Returns json response object containing all timeslots

    Args:
        None

    Retrun:
        response: json response object with all registered timeslots
        status: HTTP response code 

    """
    response, status = jsonify({}), 400

    # Ensures that only json content_type is accepted 

    if request.content_type.startswith('application/json'):
        ID, password = request.get_json().values()
        response = jsonify(clockin = AccessController.clock_in(ID, password))
        status = 200
    return response, status 
