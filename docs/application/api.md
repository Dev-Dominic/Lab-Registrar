# API /endpoints and responses 

## Usage

Response Object

```json
{
    'data': 'Mixed type holding the content  of the response', 
    'message': 'description' 
}
```

Subsequent response definitions will only detail the expected value of the *data field*

### Master Schedule 

**Definitions**

`GET /schedule/master`

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
