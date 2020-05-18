# Application Modules

from app import db
# from app.classes.models.request import SwapRequest, UserRequest
from app.classes.models.clockin import ClockInEntry, TemporarySwap

# Flask Modules

from werkzeug.security import generate_password_hash

NAME_LEN = 35
PASSWORD_HASH_LEN = 256


class UserMixin(object):  # TODO Make an abstract class
    """Mixin that models basic user for the system

    Attributes:
        uwiIssuedID
        firstname
        lastname
        password
        isAdmin
        request

    """
    uwiIssuedID = db.Column(
        db.String(10), primary_key=True, autoincrement=False)
    firstname = db.Column(db.String(NAME_LEN), nullable=False)
    lastname = db.Column(db.String(NAME_LEN), nullable=False)
    password = db.Column(db.String(PASSWORD_HASH_LEN), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, ID, firstname, lastname, password, isAdmin=False):
        """ UserMixin Constructor """
        self.uwiIssuedID = ID
        self.firstname = firstname
        self.lastname = lastname
        self.password = generate_password_hash(password)
        self.isAdmin = isAdmin

    def __repr__(self):
        """ User Object string representation """
        return f'<User: {self.fullname}>'

    @property
    def fullname(self):
        """ Returns a user's fullname """
        return f'{self.firstname} {self.lastname}'

    @property
    def user_initials(self):
        """ Returns a user's initials """
        return f'{self.firstname[0]}{self.lastname[0]}'

    def filter_user(self, filter_list):
        """Returns filtered dictionary of user attributes

        Args:
            self: instance object
            filter_list: list of attributes required

        Return:
            user_data: user filtered dictionary 

            {
                key : 'value',
                'firstname' : 'Bruce',
                'initials' : 'BH'
            }

        """
        # Filtering of query response using filter_list
        # Checks that attr is in the object's attribute/method dictionary  
        # vars method used to dynamically access class attributes

        user_data = {}
        for attr in filter_list:
            if attr in self.__dict__:
                user_data[attr] = vars(self)[attr]

            # Checks for user_initials and fullname properties because they
            # do not appear in the dictionary generated from vars

            if attr == 'user_initials':
                user_data[attr] = self.user_initials

            if attr == 'fullname':
                user_data[attr] = self.fullname 

        return user_data

    # LoginManager necessary methods

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uwiIssuedID


class User(UserMixin, db.Model):
    """User model that represents a generic user in the lab system

    Attributes:
        inheritted from UserMixin

    """
    __tablename__ = 'users'

    swap_request = db.relationship('SwapRequest', backref='admin')

    def __init__(self, ID, firstname, lastname, password, isAdmin=False):
        """ User Constructor """
        UserMixin.__init__(self, ID, firstname, lastname, password, isAdmin)


class LabTech(UserMixin, db.Model):
    """Models lab techs in the system

    Attributes:
        hours_worked: keeps track of the hours worked for a given lab tech based
        on each time they clock-in and the hours that persist after each
        clock-in

    """
    __tablename__ = 'labtechs'

    hours_worked = db.Column(db.Integer, nullable=False)

    # Model Relationships
    user_request = db.relationship(
        'UserRequest', backref='labtech', lazy='select')
    clock_in_entry = db.relationship(
        'ClockInEntry', backref='labtech', lazy='select')
    temp_swap = db.relationship('TemporarySwap', backref='labtech',
                                lazy='select')

    def __init__(self, ID, firstname, lastname, password, hours_worked):
        UserMixin.__init__(self, ID, firstname, lastname, password)
        self.hours_worked = hours_worked

    def get_hours_worked(self):
        """ hours_worked getter """
        return self.hours_worked

    def inc_hours_worked(self):
        """ Increments hours_worked by 1 """
        self.hours_worked += 1
