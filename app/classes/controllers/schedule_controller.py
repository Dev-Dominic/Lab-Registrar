# Application Modules

from app import db
from app.classes.models.user import LabTech
from app.classes.models.timeslot import TimeSlot
from app.classes.controllers.utils import is_admin, find_user

class ScheduleController:

    @staticmethod
    def __generate_schedule(timeslots):
        """Generates dictionary containing timeslots information

        Args:
            timeslots: list of timeslot instances

        Return:
            result: dictionary containing a that contain individual timeslot
            data in another dictionary

        """
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
            labtech = LabTech.query.filter_by(uwiIssuedID=labtech_id).first()
            timeslots = labtech.timeslots.all()
            result = ScheduleController.__generate_schedule(timeslots)
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
        result = ScheduleController.__generate_schedule(timeslots)
        return result

    @staticmethod
    def schedule_register(labtech_id, timeslot_id):
        """Establishes a new relationship between labtech and timeslot

        Args:
            labtech_id: labtech identifier
            timeslot_id: timeslot identifier

        Return:
            result:
                success: boolean indicating operation success
                message: message indicating why operation success state was
                given

        """
        result = {'success': False, 'message': ''}

        # Queries for a given timeslot and retrieves all labtech instances and
        # filters out the uwiIssuedID into assoc_labtechs_id

        timeslot = TimeSlot.query.filter_by(id=timeslot_id).first()
        assoc_labtechs_id = [labtech.uwiIssuedID for labtech in
                          timeslot.labtechs.all()]

        # Checks if the labtech is already associated with timeslot
        # Appends labtech instance to timeslot labtech

        if not labtech_id in assoc_labtechs_id:
            timeslot.labtechs.append(find_user(labtech_id))
            db.session.commit()

            result['success'], result['message'] = True, 'Successfully Registered timeslot'
        else:
            result['success'], result['message'] = False, 'Already registered for this timeslot'
        return result
