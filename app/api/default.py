# Application Modules

from app.classes.controllers.schedule_controller import ScheduleController

# Flask Modules

from flask import Blueprint, jsonify

default = Blueprint('default', __name__) 

@default.route('/schedule/master', methods=['GET'])
def master_schedule(): 
    """Returns json response object containing all timeslots

    Args:
        None

    Retrun:
        response: json response object with all registered timeslots
        status code: HTTP response code 

    """
    response = jsonify(ScheduleController.generate_master_schedule())
    return response, 200 
