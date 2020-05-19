# Application Modules

from app.classes.models.user import LabTech
from app.classes.models.timeslot import TimeSlot
from app.classes.controllers.utils import is_admin

class ScheduleController:

    @staticmethod
    def generate_schedule(user_request_id, labtech_id):
        """Generates labtech specific schedule

        Args:
            user_request_id: user that is requesting to generate schedule
            labtechID: labtech identifier

        Return:
            result: dictionary containing all labtech timeslots

            {
                timeslot.id: {
                    day
                    time
                    event_name
                }
            }

        """
        result = {}

        # Ensures that user that is requesting a specific schedule is the given
        # user or is an admin

        if user_request_id == labtech_id or is_admin(user_request_id):
            labtech = LabTech.query.filter_by(uwiIssuedID=labtechID).first()
            timeslots = labtech.timeslots.all() 

            result = {
                timeslot.id : {
                    'day' : timeslot.day,
                    'time' : timeslot.time,
                    'event' : timeslot.event.event_name
                }
                for timeslot in timeslots
            } 
        return result

    @staticmethod
    def generate_master_schedule():
        """Generates a general purpose schedule containing all timeslot
        information

        Args: None

        Return:
            result: dictionary containing all timeslots stored

            {
                timeslot.id: {
                    day
                    time
                    event_name
                    labtechs: ['DH', 'DC', 'TT', 'SJ', 'BT', 'JS']
                }
            }

        """
        timeslots = TimeSlot.query.all()        

        result = {
            timeslot.id : {
                'day' : timeslot.day,
                'time' : timeslot.time,
                'event' : timeslot.event.event_name,
                'labtechs' : [ labtech.user_initials for labtech in timeslot.labtechs.all() ]
            }
            for timeslot in timeslots
        } 
        return result
