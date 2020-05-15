## Updates to OOD Project Class Diagram

1. Update how requests happen for lab techs, currently doesn't show how two lab techs
interact when it comes on to swapping hours.

2. Add Master Schedule, which would display all the timeslots and events and
all the lab techs associated with each timeslot for this schedule.

3. Update relationship between Lab Tech Schedule to be composition

4. Possible changes to visiblity of Login methods

5. Changes to configureUserSession operation to add parameters(Possible use of ID)

6. updateLabTechHours() -> updateHours(ID)

7. Ommit Schedule objects and create a ScheduleHanlder object
    - generateSchedule(ID)
    - generateMsSchedule() *Master Schedule*

## During construction of Sequence diagram

8. Admin feature: generatePassword(ID)

10. Create an association between LabTechs and TimeSlots

11. Addition of ID and password parameters to Clock-in

12. verifyClockIn() => verifyClock(ID)


## Updates to OOD Project Class Diagram(May 15, 2020)

- Create UserController that can be used to retrieve user data
    - Should allow for the registering of a new user/labtech (should only allow admin to register new users)
    - Should allow for user data to be retrieved (sends all user data about a user ommitting password)

- Create Utils class diagram

- Possible Registration Controller, that handles how labtechs register for
timeslots
    - Register(labtechID, timeslotID)
    - de-register(labtechID, timeslotID)
