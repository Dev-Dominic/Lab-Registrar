# Python Modules

from random import randint

# Application Modules

from app.classes.models.user import User, LabTech
from app.classes.models.timeslot import TimeSlot

# Flask Modules

from werkzeug.security import check_password_hash, generate_password_hash

def is_admin(ID):
    """Determines whether a user/labtech is an admin

    Args:
        ID: user/labtech identifier used to query

    Return:
        is_valid_admin: boolean if a given user is an admin

    """
    is_valid_admin = False

    # First queries User database because it's the most likely place an admin
    # would appear first. Then checks LabTech table/model

    query_user = User.query.filter_by(uwiIssuedID=ID).first()
    if query_user:
        is_valid_admin = query_user.isAdmin
    else:
        query_user = LabTech.query.filter_by(uwiIssuedID=ID).first()
        if query_user:
            is_valid_admin = query_user.isAdmin

    return is_valid_admin

def timeslot_match(labtechID, timeslotID):
    """Validates that both labtech and timeslot have a relationship

    Args:
        labtechID: labtech identifier
        timeslotID: timeslot identifier

    Return
        match: boolean indicating relationship

    """
    timeslot = TimeSlot.query.filter_by(id=timeslotID).first()
    match = labtechID in [labtech.uwiIssuedID for labtech in timeslot.labtechs.all()]
    return match

def generate_password(userInitials):
    """Generates new password for a user

    Args:
        userInitials

    Return:
        password: newly generate password, returns none to indicate password was
        not generated.

    """
    if len(userInitials) != 2:
        return None

    random_num = randint(100, 999)
    password = generate_password_hash(f'{userInitials}{random_num}')
    return password

def find_user(ID):
    """Verification of user using id and password

    Args:
        ID: user/labtech identifier

    Return:
        query_user:  user instance

    """
    # Retrieving user data by checking both the User and LabTech models/tables.

    query_user = User.query.filter_by(uwiIssuedID=ID).first()
    if not query_user:
        query_user = LabTech.query.filter_by(uwiIssuedID=ID).first()

    return query_user

def verify_user(ID, password):
    """Verification of user using id and password

    Args:
        ID: user/labtech identifier
        password

    Return:
        verified: boolean indicating whether verification was successful

    """
    verified = False
    response = find_user(ID) # tuple(boolean, User Object)

    if response[0]:
        verified = check_password_hash(response[1].password, password)

    return verified

def get_user(ID, request_list):
    """Creates filtered user data dictionary

    Args:
        ID: user/labtech identifier
        request_list: filter list

    Return:
        user_data: filtered user object, that is stored in a dictionary

        {
            key : 'value',
            'firstname' : 'Bruce',
            'initials' : 'BH'
        }

    """
    user_data = {}
    response = find_user(ID)

    # Filtering of query response using request_list
    # Object dict donder method used to dynamically access
    # class attributes

    if reponse:
        for filter_el in request_list:
            user_data[filter_el] = response.__dict__(filter_el)
    return user_data
