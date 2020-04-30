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


