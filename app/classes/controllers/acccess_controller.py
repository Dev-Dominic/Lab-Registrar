# Python Modules

from datetime import datetime

# Application Modules

from app.classes.controllers.utils import verify_user, find_user

# Flask Modules

from werkzeug.security import check_password_hash

class AccessController():
    """ Handles user access to the system """

    @staticmethod
    def login(ID, password):
        """Handles normal user login and session handling

        Args:
            ID: user identifier
            password: related user instance password

        Return:
            success: boolean indicating success of the operation

        """
        pass

    @staticmethod
    def clock_in(ID, password):
        """Handles normal user login and session handling

        Args:
            ID: user identifier
            password: related user instance password

        Return:
            success: boolean indicating success of the operation

        """
        success = False
        if verify_user(ID, password):
            labtech = find_user(ID)

            # Retrieves current weekday and hour using datetime object

            date_obj = datetime.today()
            ct = (date_obj.weekday + 1, date_obj.hour) # current date and time
            timeslot = TimeSlot.query.filter_by(day=ct[0], time=ct[1])

            if timeslot and:
                labtech.hoursworked += 1
                success = True

        return success

