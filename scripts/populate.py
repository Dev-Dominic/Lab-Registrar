# Python Modules

from random import randint

# Application Modules

from app import db
from app.classes.models.user import User, LabTech
from app.classes.models.timeslot import Event, TimeSlot
from app.classes.models.request import UserRequest, SwapRequest

def create_admin():
    """ Creates user instances that are models """
    bruce = User('60000000', 'Bruce', 'Hoo-Fung', 'password', True)
    kerry = User('60000001', 'Kerry', 'Thompson', 'password', True)
    paul = User('60000002', 'Paul', 'Coleman', 'password', True)

    db.session.add(bruce)
    db.session.add(kerry)
    db.session.add(paul)

    db.session.commit()

def create_labtechs():
    """ Creates labtech instances that are models """
    dominic = LabTech('620118591', 'Dominic', 'Henry', 'password', 0)
    tahjyei = LabTech('60000003', 'Tajhyei', 'Thompson', 'password', 12)
    dineah = LabTech('60000004', 'Dineah', 'Cohen', 'password', 4)
    shaun = LabTech('60000005', 'Shaun', 'Jennings', 'password', 0)
    brandon = LabTech('60000006', 'Brandon', 'Tucker', 'password', 24)
    jamar = LabTech('60000007', 'Jamar', 'Salmon', 'password', 0)

    db.session.add(dominic)
    db.session.add(tahjyei)
    db.session.add(dineah)
    db.session.add(shaun)
    db.session.add(brandon)
    db.session.add(jamar)
    
    db.session.commit()

def create_events():
    """ Creates event instances """
    free_hour = Event('Free Hour')
    comp1126 = Event('LAB COMP1126') 
    comp1127 = Event('LAB COMP1127') 
    comp1161 = Event('LAB COMP1161') 
    comp2340 = Event('LAB COMP2340') 

    db.session.add(free_hour)
    db.session.add(comp1126)
    db.session.add(comp1127)
    db.session.add(comp1161)
    db.session.add(comp2340)

    db.session.commit()

def create_timeslots():
    """ Creates timelot instances and randomize events for each """
    for day in range(1,6):
        for time in range(8,19):
            timeslot = TimeSlot(day, time, randint(1,5))
            
            # Randomly adds labtechs to the timeslot
            # Stores a record of labtechs already associated with timeslot
            # To ensure no duplication of relationships

            record = []
            for _ in range(1,randint(1,7)):
                current_choice = randint(0,5)
                if current_choice in record:
                    continue
                timeslot.labtechs.append(LabTech.query.all()[current_choice]) 
                record.append(current_choice)

            db.session.add(timeslot)
    db.session.commit()

if __name__ == "__main__":
    create_admin()
    create_labtechs()
    create_events()
    create_timeslots()
