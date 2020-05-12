# Controllers 

Controller classes should have checks that ensure that data is consistent
throughout what the models store.

## Util methods

**isAdmin**

**TimeSlotMatch**

Ensures that a given labtech matches a given timeslot.

1. Accepts both labtech and timeslot identifiers.
2. Makes query to timeslot database controller 
3. Determines whether the labtech's identifier is associated with the timeslot

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


**Request Swap**

1. Use *TimeSlotMatch* to determine whether labtech corresponds with a given
   timeslot. 
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

## Access Controllers

#### Login

#### Clock-in

## Other

#### ScheduleController

