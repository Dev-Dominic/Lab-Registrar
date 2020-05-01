## Presentation Script

## Class Diagram

This is the updated Class Diagram for our Lab Tech Registrar System

Previously we had a General Schedule and Lab Tech Schedule classes, which we
omitted in favor of a ScheduleHanlder class that generates specific master schedules
based on a given userID(Lab Tech), as well as, generates a Master Schedule. 

A further association was also made between the Lab Tech and TimeSlot class,
where there is 0 to many mulitplicty between both classes. This association was
made because we would need to know when a given lab tech works, as well as,
associated it is necesarry assocaition for when a schedule is generated to know
which timeSlots are related to a given Lab Tech.


## Sequence Diagrams

**Request new password**

During the request for a new password both a Lab Tech and Admin users interact. 
labTech makes a password request, as well as, sending an ID so that the Admin
knows what lab tech is making the request. Admins generate the new password 
and the password is sent as a reply to the lab tech.

**Request temporary swap**

Three actors interact during this process, the lab tech making the request,
another lab tech that confirms that they want to make a swap, as well as, an admin
that approves swap. A requestSwap() message is sent to a lab tech, where
they confirm that they would like to swap would be sent to both the previous lab tech
and an admin. Both ID's of the related lab techs are sent to the Admin. The admin
makes an approval and the an approval message is sent to both lab techs.

**Schedule**

This details how a Lab Tech or admin may request a lab tech schedule. 

To create a schedule needed be a user, a user must first use the generateSchedule
method from a ScheduleHanlder that also takes an ID. Thereafter, the ScheduleHanlder
makes a request to the TimeSlot to receive all the related timeslots with a given
Lab Tech ID. TimeSlot replies to ScheduleHanlder with the list of related timeslots.
Where the ScheduleHanlder creates a formated schedule that is sent to the User.

**Clock-in**

user makes requests to Clock-in with an ID and password as parameters. Clock-in 
will then verify the user by using the Lab Tech class and verification message is
sent to Clock-in, were it then also verifies that a given user is eligible to clock-in
by querying their ID for a given TimeSlot. Once verified a message is sent to both the
Clock-in and the user. 
