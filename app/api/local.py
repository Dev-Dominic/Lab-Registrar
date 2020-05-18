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

    if request.content_type.startswith('application/json'):
        ID = request.args.get('uwiIssuedID')
        password = request.args.get('password')
        response = jsonify(AccessController.clock_in(ID, password))
        status = 200
    return response, status 
