## Presentation Three(3) Feedback

### Feedack

- First two forcing classes to works to be done by controllers

- Controller for requesting password

- Diagrams are accurate

- Transactions controlled by controllers

- Add attributes to objects in diagrams

- Create different classes that controlles data between different objects in the
system.

- Take off burden off admin and lab tech classes

- Add more attributes to give more context as to how objects relate in the
Object Diagram at a given state.

- Update names for Object Diagrams, something that reflects

- Break up request temporary swap, one for requesting a swap and one for
confirming a swap.

### Possible Updates Summarize

- Creation of Database Class

- Creation hanlder class for changing of data between Admin and Lab Tech

- DatabaseController(Flask SQLAlchmey database class):
 the purpose of this is to model how Flask and SQLAlchmey
 are used in typical flask projects that utilize a database,
 DatabaseController class only has one method called
 query.

- Update names of Objects/Instances in Object and Sequence Diagram

- Addition of attributes to Object in Object Diagrams to give
context as to what is occuring in that even given instance.

- Break Request temporary swap into two sequence diagrams:
    1. Requesting Swap
    2. Swap Confirmation

- Remove multiplicies from Object Diagram

- Determine design pattern to use

### Updates

#### Class Diagram

- DatabaseController subclasses:
    1. User:
        - Add field named isAdmin
        - Add getHoursWorked method
        - Remove Admin subclass
        - LabTech subclass:
            - hoursWorked
    2. TimeSlots
    3. Events
    4. Request(Stores Lab Tech requests)
        - id
        - userRequestID (user that makes the request)
        - status
        - Sub-classes:
            - SwapRequest
                - userConfirmID
                - adminID
                - userTimeSlotOne
                - userTimeSlotTwo
            - UserRequest
                - infotype
                - newInfo
            - NewPasswordRequest
    5. TemporarySwap(Stores temporary timeslot swaps between two labtechs)
        - id
        - labtechID
        - timeslotID

- Class Handlers(Singletons):
    1. Login
    2. Clock-in(Inherits Login for verfication functionality)
    3. RequestHandler
        - checkstate
        - resolve
        - Sub-classes
        - SwapRequestHandlder
        - UserRequestHandlder
    4. ScheduleHandler(Used to generate Lab Tech Schedules and Master Schedules)
        - Creates Schedule instance
            - Stores specific lab tech schedule
        - Makes use of TimeSlots DatabaseController
        - staticmethod for creating MasterSchedule

- User Inteface Classes:
    - UserInterface parent class?
    - LoginUI
    - ClockInUI
    - RegistrationUI(Requires real-time schedule to be generated)
    - ViewMasterScheduleUI
    - userScheduleUI(Lab Tech personalized schedule)
    - requestSwapUI (Global page that shows all requests)
        - Limit confirm and request options to lab techs
        - Only show approval option for admin accounts
    - AdminUI
        - Main: List of currently working lab tech
        - View: Lab tech details(hours worked, etc)

#### Sequence Diagrams

- Request new password:
    -

### Notes

- Controllers should only be responsible for creating, deleting and updating
data.

- Handlers deal with the logical aspects such as authentication and how things
are done.

##### Deciding Design pattern
    1. Facade: Section of certain part of into a subsystem

    2. Template: Used class extended to create Admin and Lab Tech classes

    3. Adapter: Possible use in developing UserInteface

    4. Singletons: Possible use for developing handler classes that possible may
        only need one instace

#### Other updates
