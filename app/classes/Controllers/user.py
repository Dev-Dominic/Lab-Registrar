from app import db
from werkzeug.security import generate_password_hash

NAME_LEN = 35
PASSWORD_HASH_LEN = 256

class User(db.Model):
    """Models basic user for the system

    Attributes: 
        uwiIssuedID
        firstname
        lastname
        password
        isAdmin

    """
    __tablename__='users'
    
    uwiIssuedID = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(NAME_LEN), nullable=False)
    lastname = db.Column(db.String(NAME_LEN), nullable=False)
    password = db.Column(db.String(PASSWORD_HASH_LEN), nullable=False)  
    isAdmin = db.Column(db.Boolean, nullable=False, default=False) 

    def __init__(self, ID, firstname, lastname, password):
        """ User Constructor """
        self.uwiIssuedID = ID
        self.firstname = firstname
        self.lastname = lastname
        self.password = generate_password_hash(password)

    def __repr__(self):
        """ User Object string repersentation """
        return f'<User {self.fullname()}>' 

    def fullname(self):
        """ Returns a user's fullname """
        return f'{self.firstname} {self.lastname}'

    def user_initials(self):
        """ Returns a user's initials """
        return f'{self.firstname[0]}{self.lastname[0]}'

class LabTech(User):
    """Models lab techs in the system

    Attributes:
        hoursWorked: keeps track of the hours worked for a given lab tech based
        on each time they clock-in and the hours that persist after each
        clock-in

    """
    __tablename__= 'labtechs'

    hoursWorked = db.Column(db.Integer, nullable=False)

    def __init__(self, ID, firstname, lastname, password, hoursWorked):
        super().__init__(ID, firstname, lastname, password)
        self.hoursWorked = hoursWorked
