# User 

Documents all the user related API requests

## API authentication (Login)

**Definitions**

`POST /web/auth/login`

**Arguments**

- `uwiIssuedID`: 6000000
- `password`: password

**Response**

- `200 OK` on success
-  `500 Internal Server Error` an exception occurred while processing request
- `400 Bad Request` if end request sent is invalid

```json
{
    access_token: '29HLJkjdl092dj.929jfdjalkdjf.09i0f2k'
}
```

## Create user

**Definitions**

`POST /web/newuser`

**headers**

- `Authorization`

**Arguments**

- `uwiIssuedID`
- `firstname`
- `lastname`
- `labtech`: boolean 
- `Admin`: boolean

**Response**

- `201 Created` on success
- `200 OK` indicating that the resource was not created

```json
{
    create_newuser: 'true' / 'false'
}

```

## Clockin

**Definitions**

`POST /local/clockin`

**Arguments**

- `uwiIssuedID`: 6000000
- `password`: password

**Response**

- `200 OK` on success
- `500 Internal Server Error` an exception occurred while processing request
- `400 Bad Request` if end request sent is invalid

```json
{
    clockin: 'true' / 'false'
}
```

## Get User (filter results)

**Definitions**

`GET /web/user (should send filter_list in json request)`

**headers**

- `Authorization`

**Parameters**

- `uwiIssuedID`: 6000000

**Response**

- `200 OK` on success
- `403 Forbidden` unauthorized user accessing endpoint

```json
{
    'uwiIssuedID': 6000000,
    'firstname': 'John',
    'lastname': 'Doe',
    'fullname': 'John Doe',
    'user_initials': 'JD', 
    'hours_worked': 2,
}
```

**Note**: Invalid entries and an empty request_list will only return an empty
response object.

## Get all users

**Definitions**

`GET /web/users`

**Response**

- `200 OK` on success

```json
{
    6000000: {
        'firstname': 'John',
        'lastname': 'Doe',
        'user_initials': 'JD',
        'Admin': 'false'
    },
    650000: {
        'firstname': 'Dineah',
        'lastname': 'Cohen',
        'user_initials': 'DC',
        'Admin': 'true'
    }
}
```

## Get currently working labtechs

**Definitions**

`GET /default/labtech/working`

**Response**

- `200 OK` on success

```json
{
    1: {
        'fullname': 'John Doe',
        'user_initials': 'JD'
    },
    2: {
        'fullname': 'Dineah Cohen',
        'user_initials': 'DC',
    }
}
```
