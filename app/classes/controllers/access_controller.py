# Python Modules

from datetime import datetime

# Application Modules

from app import db
from app.classes.models.user import LabTech
from app.classes.models.timeslot import TimeSlot
from app.classes.models.clockin import ClockInEntry
from app.classes.controllers.utils import verify_user, find_user, timeslot_match

class AccessController():
    """ Handles user access to the system """

    @staticmethod
    def authenticate(ID, password):
        """User authentication 
        
        Args:
            ID: user/labtech identifier
            password: associated user/labtech password

        Return:
            user: user model instance

        """
        user = find_user(ID)
        if user and verify_user(ID, password):
            # Additional property added to user instance object for the purpose
            # of JWT payload that requires an `id` property 

            user.id = user.uwiIssuedID
            return user

    @staticmethod
    def identity(payload):
        """Uses payload information to retrieve current user

        Args:
            payload: contains persisted user id (uwiIssuedID) 

        Return: 
            user: user model instance

        """
        uwiIssuedID = payload['identity']
        return find_user(uwiIssuedID)

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
            ct = [date_obj.weekday() + 1, date_obj.hour] # current date and time
            timeslot = TimeSlot.query.filter_by(day=ct[0], time=ct[1]).first()

            # Checks that timeslot exists along with whether a given labtech is
            # associated with timeslot 

            if timeslot and timeslot_match(labtech.uwiIssuedID, timeslot.id):
                labtech.inc_hours_worked()
                new_clockin_entry = ClockInEntry(labtech.uwiIssuedID, timeslot.id) 

                db.session.add(new_clockin_entry)
                db.session.commit()
                success = True

        return success
