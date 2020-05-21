# API Documentation

## Endpoints

1. Users
    - POST /web/auth/login
    - POST /local/clockin
    - POST /web/newuser (only allows admin to create new user)
    - GET /web/user
    - GET /web/users (all users)
    - GET /default/labtech/working (gets currently working labtechs)
<br>
2. Schedules
    - GET /default/schedule/master
    - GET /web/schedule/
    <br>
    **Admin endpoints used to configure timeslots and events**
    - POST /web/schedule/register/timeslots
    - POST /web/schedule/register/events
    <br>
    **Handles labtech registration for timeslots**
    - POST /web/schedule/register
<br>
3. SwapRequest
    - GET /web/request/swap
    - GET /web/requests/swap
    - POST /web/request/swap
    - PATCH /web/request/swap/accept
    - PATCH /web/request/swap/approve
<br>
4. UserRequest
    - GET /web/request/user
    - POST /web/request/user
    - PATCH /web/request/user/approve

**Note**: Possible Security issues with using `GET` method to get data from API.

## Usage

Response Object

```json
{
    'data': 'Mixed type holding the content  of the response',
    'message': 'description'
}
```

- Subsequent response definitions will only detail the expected value of the *data field*
- All requests made using arguments should be done using json objects

**Request Catagories**

- [Users](user_api.md)
- [Schedules](schedule_api.md)
- [Requests](requests_api.md)
