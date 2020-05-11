# Python Modules

import enum

# Applicaiton Modules

from app import db

class Status(enum.Enum):
    OPEN = enum.auto()
    DENIED = enum.auto()
    CONFIRM = enum.auto()
    APPROVED = enum.auto()

class RequestMixin(object):  
    """Contains necesarry attributes for various request controller classes

    Attributes:
        id: request identifier
        status: status enum value detailing current status of a request
        
    """
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status))

    def __init__(self, status, labtech_request_id):
        """ Request Constructor """
        self.status = status
        self.labtech_request_id = labtech_request_id

    def __repr__(self):
        """ Request Object string repersentation"""
        return f'<Request: {self.id} {self.status}'

class SwapRequest(RequestMixin, db.Model):
    """Stores swap requests

    Attributes:
        inherited from RequestControllerMixin

    """
    
    # Foreign Column Relationships

    # User and LabTech Relationships
    # Establishes multiple labTech database reference by using a db relationship

    labtech_request_id = db.Column(db.Integer,
                                   db.ForeignKey('labtechs.uwiIssuedID')) 
    labtech_confirm_id = db.Column(db.Integer, 
                                   db.ForeignKey('labtechs.uwiIssuedID')) 
    admin_approve_id = db.Column(db.Integer, db.ForeignKey('users.uwiIssuedID')) 

    labtech_request = db.relationship('LabTech', foreign_keys=labtech_request_id)
    labtech_confirm = db.relationship('LabTech', foreign_keys=labtech_confirm_id)

    # TimeSlot Relationships
    # Establishes multiple timeslot database reference by using a db relationship

    request_labtech_timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'))
    confirm_labtech_timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'))

    request_labtech_timeslot = db.relationship('TimeSlot',
                                               foreign_keys=request_labtech_timeslot_id)
    confirm_labtech_timeslot = db.relationship('TimeSlot',
                                               foreign_keys=confirm_labtech_timeslot_id)
     
    def __init__(self, status, labtech_request_id, request_labtech_timeslot_id):
        """ SwapRequest Constructor """
        RequestMixin.__init__(self, status, labtech_request_id)
        self.request_labtech_timeslot_id = request_labtech_timeslot_id
