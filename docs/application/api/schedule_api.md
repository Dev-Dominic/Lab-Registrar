# Schedule

Documents all the schedule related API requests

## Master Schedule 

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

## Labtech Schedule

`GET /web/schedule`

**Header**

- `Authorization`

**Response**

- `200 OK` on success
- `403 Forbidden` if request by unauthorized user

```json
{
    30 : {
        'day' : 3,
        'time' : 15,
        'event' : 'COMP1126',
    },
    40 : {
        'day' : 5,
        'time' : 20,
        'event' : 'COMP1126',
    },
}
```

## LabTech Registration

`PATCH /web/schedule/register `

**Header**

- `Authorization`

**Arguments**

- `timeslot_id` 

**Response**

- `200 OK` on success
- `400 Bad Request` bad request body

```json
{
    success: true / false,
    message: message indicating what caused success to be true or false
}
```
