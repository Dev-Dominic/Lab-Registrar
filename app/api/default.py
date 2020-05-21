# Application Modules

from app.classes.controllers.schedule_controller import ScheduleController
from app.classes.controllers.utils import clocked_in

# Flask Modules

from flask import Blueprint, jsonify

default = Blueprint('default', __name__) 

@default.route('/schedule/master', methods=['GET'])
def default_master_schedule(): 
    """Returns json response object containing all timeslots

    Args:
        None

    Retrun:
        response: json response object with all registered timeslots
        status code: HTTP response code 

    """
    response = jsonify(ScheduleController.generate_master_schedule())
    return response, 200 

@default.route('/labtech/working')
def default_labtech_working():
    """Returns json response object containing all currently working labtechs

    Returns labtech initials and uwiIssuedID

    Args:
        None

    Return:
        response: json response object with all working labtechs
        status: HTTP response code

    """
    response, status = jsonify({}), 400

    clock_in_labtechs = clocked_in()
    if clock_in_labtechs:
        response, status = jsonify(clock_in_labtechs), 200

    return response, status

