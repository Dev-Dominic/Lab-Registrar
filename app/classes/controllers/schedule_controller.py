# Python Modules

# Application Modules

from app.classes.models.timeslot import TimeSlot
from app.classes.controllers.utils import verify_user

# Flask Modules

class ScheduleController:

    @staticmethod
    def generate_schedule(labtechID):
        """Generates labtech specific schedule

        Args:
            labtechID: labtech identifier

        Return:
            result: json object containing all labtech timeslots

            {
                timeslot.id: {
                    day
                    time
                    event_name
                }
            }

        """
        pass

    @staticmethod
    def generate_master_schedule():
        """Generates a general purpose schedule containing all timeslot
        information

        Args: None

        Return:
            result: json object containg all timeslots stored

            {
                timeslot.id: {
                    day
                    time
                    event_name
                    labtechs: ['DH', 'DC', 'TT', 'SJ', 'BT', 'JS']
                }
            }

        """
        pass
