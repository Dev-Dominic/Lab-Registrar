# Python Modules

from datetime import datetime

# Application Modules

from app import db
from app.classes.models.user import User, LabTech
from app.classes.models.timeslot import TimeSlot
from app.classes.models.clockin import ClockInEntry
from app.classes.controllers.utils import verify_user, find_user, timeslot_match

# Flask Modules

from flask_login import login_user
from app import login_manager
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
        success = False
        if verify_user(ID, password):
            labtech = find_user(ID)
            login_user(labtech)
            success = True
        return success

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
            ct = (date_obj.weekday() + 1, date_obj.hour) # current date and time
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

    @login_manager.user_loader
    @staticmethod
    def load_user(user_id):
        return find_user(user_id)
