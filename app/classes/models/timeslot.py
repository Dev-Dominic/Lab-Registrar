# Application Modules

from app import db
from app.classes.models.user import LabTech

# Flask Modules

NAME_LEN = 100 

class Event(db.Model):
    """Stores various events that occur while the lab is open

    Attributes:

    """
    __tablename__='events'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(NAME_LEN))
    timeslots = db.relationship('TimeSlot', backref='event', lazy='select')

    def __init__(self, event_name):
        """ Events Constructor """
        self.event_name = event_name

    def __repr__(self):
        """ Event Object string repersentation """
        return f'<Event {self.id}:{self.event_name}>'

# Establishes many to many relationship between LabTech and  TimeSlot Object

labtechs = db.Table(
    'labtech_timeslot',
    db.Column('timeslot_id', db.Integer, db.ForeignKey('timeslots.id'),
              primary_key=True),
    db.Column('labtech_id', db.Integer, db.ForeignKey('labtechs.uwiIssuedID'),
              primary_key=True)
)

class TimeSlot(db.Model):
    """Stores all availabe timeslots for a given lab

    Attributes: 
        id: unique identifier for timeslot
        day: associated day of the week 
        time: associated time of day for timeslot 
        event: associated event 

    """
    __tablename__='timeslots'
    
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False) 
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), default=1,
                         nullable=False)
    labtechs = db.relationship('LabTech', secondary=labtechs, lazy='dynamic',
                            backref=db.backref('timeslots', lazy='dynamic'))

    def __init__(self, day, time, event_id):
        self.day = day
        self.time = time
        self.event_id = event_id
