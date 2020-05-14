# Python Modules

from datetime import datetime

# Application Modules

from app import db


class ClockInEntry(db.Model):
    """Stores every labtech that signs in within a given timeslot period

    Attributes:
        id: entry identifier
        labtech_id: identifier of labtech that has clocked-in
        timeslot_id: identifier of timeslot to which the labtech has clocked into
        date_time: datetime denoting when the labtech has clocked-in

    """
    id = db.Column(db.Integer, primary_key=True)
    labtech_id = db.Column(
        db.String(10), db.ForeignKey('labtechs.uwiIssuedID'))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'))
    date_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, labtech_id, timeslot_id):
        """ ClockInEntry Constructor """
        self.labtech_id = labtech_id
        self.timeslot_id = timeslot_id
        self.date_time = datetime.now()

# TODO implement expiration for a temporary swap
class TemporarySwap(db.Model):
    """Stores data used to determine whether a user is eligible to clock-in at a
    given time

    Attributes:
        id: TemporarySwap identifier
        labtechID: associated labtech identifier
        timeslotID: associated timeslot identifier

    """
    id = db.Column(db.Integer, primary_key=True)
    labtechID = db.Column(db.String(10), db.ForeignKey('labtechs.uwiIssuedID'))
    timeslotID = db.Column(db.Integer, db.ForeignKey('timeslots.id'))

    def __init__(self, labtechID, timeslotID):
        """ TemporarySwap Constructor """
        self.labtechID = labtechID
        self.timeslotID = timeslotID
