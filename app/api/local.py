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

    # Offloads json response into ID and password, should throw an exception in
    # the event that two many parameters where sent in the json object body

    try:
        ID, password = request.get_json().values()

        if ID and password: 
            response = jsonify(clockin = AccessController.clock_in(ID, password))
            status = 200
    except:
        response = jsonify(err='Server Error: Credentials Issue')
        status = 500
    
    return response, status 
