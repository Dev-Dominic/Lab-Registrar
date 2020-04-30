## System Actors/Objects

### Request new password

1. Lab Tech (many)
2. Admin (one)

### Request temporary swap

1. Request: Lab Tech (one)
2. Confirm: Lab Tech (one)
3. Approve: Admin (one)

### Schedule

1. User (many) 
2. ScheduleHandler (one) (many)
3. TimeSlot (many)

### Clock-in

1. Lab Tech (one)
2. Clock-In (one)
3. TimeSlot

## Sequence Diagrams

### Request new password

1. labTech:Lab Tech => requestNewPassword() => admin:Admin

2. admin:Admin => generatePassword(ID) => admin:Admin

3. admin:Admin => password => labtech:Lab Tech

### Request temporary swap

1. request:Lab Tech => requestSwap() => confirm:Lab Tech =>
acceptSwap() => approve:Admin 

2. approve:Admin => approveSwap(requestID, receiverID) => confirm:Lab Tech

3. approve:Admin => approveSwap(requestID, receiverID) => request:Lab Tech

### Schedule (generateSchedule)

1. user:User => generateSchedule(ID) => hanlder:ScheduleHandler => 
request timeSlosts for ID => slots:TimeSlots

2. slots:TimeSlots => timeslots => handler:ScheduleHandler => schedule 
=> user:User

### Clock-in

1. user => Clock-in(ID,password) => :Clock-in => verifyUser(ID,password) => 
:Lab Tech => verified => Clock-in => verifyClockIn(ID) => :TimeSlot =>
verifiedClock-in

2. TimeSlot => :Clock-in => user 


