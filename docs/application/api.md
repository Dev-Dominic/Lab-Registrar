# API /endpoints and responses 

## Endpoints

1. Users
    - POST /web/auth/login
    - GET /web/user (should send filter_list in json request)
    - GET /web/user
    - POST /local/clockin
    - POST /web/newuser (only allows admin to create new user)

2. Schedules
    - /default/schedule/master
    - /local/schedule/ 

3. SwapRequest
    - POST /web/request/swap/
    - PATCH /web/request/swap/accept
    - PATCH /web/request/swap/approve

4. UserRequest
    - PATCH /web/request/user/
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

## Default

### Master Schedule 

**Definitions**

`GET /default/schedule/master`

**Response**

- `200 OK` on success

```json
{
    30 : {
        'day' : 3,
        'time' : 15,
        'event' : 'COMP1126',
        'labtechs' : ['DH', 'DC', 'TT', 'SJ', 'BT', 'JS']
    },
    40 : {
        'day' : 5,
        'time' : 20,
        'event' : 'COMP1126',
        'labtechs' : ['DH', 'ND', 'JD', 'JS', 'AL']
    },
}
```

### Clockin

**Definitions**

`POST /local/clockin`

**Arguments**

- `uwiIssuedID`: 6000000
- `password`: password

**Response**

- `200 OK` on success
- `500 Internal Server Error` on exception while processing request 
- `400 Bad Request` if end request sent is invalid

```json
{
    clockin: 'true' / 'false'
}
```
