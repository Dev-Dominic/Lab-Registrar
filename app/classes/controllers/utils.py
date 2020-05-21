# Python Modules

from random import randint
from datetime import datetime

# Application Modules

from app.classes.models.user import User, LabTech
from app.classes.models.timeslot import TimeSlot
from app.classes.models.clockin import TemporarySwap, ClockInEntry

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

    Validates by searching both the labtech_timeslot relationship and
    temporary_swap table.

    Args:
        labtechID: labtech identifier
        timeslotID: timeslot identifier

    Return
        match: boolean indicating relationship

    """
    timeslot = TimeSlot.query.filter_by(id=timeslotID).first()
    labtech_timeslot = [labtech.uwiIssuedID for labtech in timeslot.labtechs.all()]
    temporary_swap = TemporarySwap.query.filter_by(labtechID=labtechID,
                                                   timeslotID=timeslotID).all()
    temp_swap_ids = [temp.labtechID for temp in temporary_swap]

    match = (labtechID in labtech_timeslot) or (labtechID == temp_swap_ids)
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

    if response:
        verified = check_password_hash(response.password, password)

    return verified

def get_user(user_request_id, labtech_id, request_list):
    """Creates filtered user data dictionary

    Args:
        ID: user/labtech identifier
        request_list: filter list

    Return:
        user_data: filtered user object, that is stored in a dictionary

    """
    user_data = {}

    # Checks that the requesting user is requesting their own data or an admin
    # is requesting the the data

    if user_request_id == labtech_id or is_admin(user_request_id):
        user_data = find_user(labtech_id).filter_user(request_list)
    return user_data

def get_users(user_request_id):
    """Gets all users stored in user and labtech model databases

    This should only allow for admins to retrieve all user data
        
    Args:
        user_request_id: user making the request
    
    Return:
        user_data: dictionary containing all users

    """
    user_data = {}
    request_list =['firstname', 'lastname', 'user_initials', 'hours_worked', 'fullname'] 
    if is_admin(user_request_id):
        users = User.query.all()       
        labtech = LabTech.query.all()

        # Creates each user/labtech instance into a dictionary entry

        entry = 1
        for user in (users + labtech):
            user_data[entry] = user.filter_user(request_list)
            entry += 1

    return user_data

def clocked_in():
    """Returns list of currently clocked in users

    Args:
        None

    Return
        clocked_in_labtechs: dictionary containing filter labtech instances tha
        t are currently clocked_in

        {
            entry_no: {
                fullname,
                user_initials
            }            
        }
    
    """
    clocked_in_labtechs = {}
    request_list = ['fullname', 'user_initials']
    date_check_format = '%Y-%m-%d-%H'

    clock_in_entries = ClockInEntry.query.all()
    current_date =  datetime.today().strftime(date_check_format)

    # Checking current_date format against clock_in_entries

    entry_no = 1
    for entry in clock_in_entries: 
        # Retrives entry_time and compares with current time to determine
        # whether a given labtech is clocked_in

        entry_time = entry.date_time.strftime(date_check_format)
        if entry_time == current_date:
            user = find_user(entry.labtech_id) 
            clocked_in_labtechs[entry_no] = user.filter_user(request_list)
            entry_no += 1

    return clocked_in_labtechs
