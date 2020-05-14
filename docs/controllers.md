# Controllers

Controller classes should have checks that ensure that data is consistent
throughout what the models store.

### Utilities 

**isAdmin**

1. Query for ID using User and Labtech models    
2. Return whether the given instance/model is an admin or not

**TimeSlotMatch**

Ensures that a given labtech matches a given timeslot.

1. Accepts both labtech and timeslot identifiers.
2. Makes query to timeslot database controller
3. Determines whether the labtech's identifier is associated with the timeslot

**Generate Password**

1. Generate pseudo-random password (using initials and random number between 100
   and 999)
2. Generate new password hash
3. Return password hash 

**Verify User**

1. Query for user in both the User and LabTech tables
    * Not Found: return false
2. Validate that the password that was passed with the password hash present in
   the table
    * Not Valid: return false
3. Once the password validation is successful return true

## Request Controllers

1. These controllers are used to store, update, delete request from the database
   tables.

2. Once each request has reached a resolved state the controller should make
   updates to the various models database.

#### RequestControllerAbstract

**CheckState**

Determines whether current request state can be resolved based on the request
status.

1. Use requestID to query a given Request Table for a request
2. Check that the state is: **DENIED** or **APPROVED**
    * Return true if **DENIED** or **APPROVED**
    * Return false otherwise

**Resolve**

Makes updates to the database through the application models.

1. Use *CheckState* to ensure that the current status of a given request is in a
   state that can be resolved.
2. Subclasses will then make necessary checks to ensure data integrity and
   consistency in the database models/tables.
3. Changes are reflected in database models/tables
4. Return true if resolve was successfully and false otherwise

#### SwapRequestController

**Dependencies**

1. Application SQLAlchemy database instance
2. Application SwapRequest model
3. TimeSlotMatch from Utils module

**Resolve**

1. Call parent class *Resolve* definition (Passing requestID)
2. Create new TemporarySwap instance, passing:
    * labtechID
    * counterTimeSlotID
3. Create new TemporarySwap instance, passing:
    * counterlabtechID
    * requestTimeSlotID
4. Add both TemporarySwap instances to database and commit changes

**Request Swap**

1. Use *TimeSlotMatch* to determine whether labtech corresponds with a given
   timeslot(requestTimeSlotID).
2. Create a new SwapRequest instance filling in the necessary details.
    - labtechID
    - request status
3. Add and commit these SwapRequest to database.

**Accept Swap**

1. Use *TimeSlotMatch* to determine that the other labtech corresponds with the
   counterTimeSlotID.
2. Update SwapRequest instance associated with swapID
    * Update fields with counterlabtechID and counterTimeSlotID
    * Update Status to confirm to indicate that labtech has affirmed to wanting
    a possible switch
3. Commit changes to SwapRequest model/database

**Approve Swap**

1. Check that adminID is a valid admin
2. Update SwapRequest instance with swapID
    * Update adminID field
    * Update status field with either **DENIED** or **APPROVED**
3. Run *Resolve*

#### UserRequestController

**Dependencies**

1. Application SQLAlchemy database instance
2. GeneratePassword from Utils module

**Resolve**

1. Call parent class *Resolve* definition (Passing requestID)
2. Check whether infoType is a password:
    * False: 
        1. Query for LabTech
    * True: 
        1. Call Utils *GeneratePassword* method 
        2. Query for LabTech instance 
3. Update labtech instance and commit changes

**Update User Data**

1. Check that the user/labtech identifier is valid
2. Create new UserRequest instance
    * labtechID
    * status to OPEN
    * infoType
    * newInfo
3. Add and commit new UserRequest to database

**Approve Request**

1. Check that ID passed is a valid adminID
2. Retrieve UserRequest instance using userRequestID 
3. Update status field with either **DENIED** or **APPROVED**
4. Run *Resolve*

## Access Controllers

**Dependencies**

1. Application SQLAlchemy database instance
2. Verify User from Utils module

#### Login

**User Login**

1. Verify User using utils module
2. Use login manager to login user 
3.  

**Configure Session**

#### Clock-in

**Verify ClockIn**

**ClockIn**

## Other

#### ScheduleController

**Dependencies**

1. Application SQLAlchemy database instance
2. Application TimeSlot, Event, LabTech model

Each method describe returns a json object with all the associated timeslots.

**Generate Schedule**

1. LabtechID validation 
2. Query TimeSlot model for all timeslots that are associated with LabTechID
3. Format list of TimeSlots into a json object
    
```json

{
    timeslot.id: {
        day  
        time
        event_name
    }
}

```

**Generate Master Schedule**

1. Query TimeSlot model for all Timeslots
2. Create a json object with timeslot information, as well as, one key : value
   pair that has a list of associated labtechs by Initials.

```json

{
    timeslot.id: {
        day
        time
        event_name
        labtechs: ['DH', 'DC', 'TT', 'SJ', 'BT', 'JS'] 
    }
}

```
