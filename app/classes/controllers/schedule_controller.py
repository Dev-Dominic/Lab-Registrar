# Python Modules

# Application Modules

from app.classes.models.user import LabTech
from app.classes.models.timeslot import TimeSlot
from app.classes.controllers.utils import is_admin

# Flask Modules

# TODO possible precautionary code to check that the person that is currently
# logged in isn't accessing other people's generated schedule

class ScheduleController:

    @staticmethod
    def generate_schedule(labtechID):
        """Generates labtech specific schedule

        Args:
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
            result: dictionary containg all timeslots stored

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
                'event' : timeslot.event.event_name
                'labtechs' : [labtech.user_initials() for labtech in
                              timeslots.labtechs.all() ]
            }
            for timeslot in timeslots
        } 
        return result
