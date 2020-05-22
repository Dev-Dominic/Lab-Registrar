# User Request

Details API endpoints for UserRequest

## Get a user request

**Definitions**

`GET /web/request/user`

**Parameters**

- `request_id`: 12

**Response**

- `200 OK` on success
- `400 Bad Request` occurs with invalid parameters
- `404 Not Found` occurs if a given request is not found

**OPEN Request**

```json
{
     "10":{
        "status": "OPEN",
        "labtech_request_id": "62011781",
        "infoType": "firstname"
        "newInfo": "charles"
        "admin_approve_id": "",
    }
}
```

**APPROVE Request**

```json
{
     "10":{
        "status": "APPROVED",
        "labtech_request_id": "62011781",
        "infoType": "firstname"
        "newInfo": "charles"
        "admin_approve_id": "6000000",
    }
}
```
## Post a request

**Definitions**

`POST /web/request/user`

**Arguments**

`Passwords are generated for a user, no newInfo parameter needed`
- "infoType" : 'PASSWORD'

`Otherwise:`
- "infoType" : 'uwiIssuedID'
- "newInfo": '600017189'

**Response**

- `201 Created` on success
- `500 Internal Server Error` issues arise on server
- `400 Bad Request` improper request parameters

**OPEN Request**

**Success**
```json
{
    "message": "Request made",
}

**Error**
```json
{
    "message": "Request could not be created",
}
```

## Get all user requests

**Definitions**

`GET /web/requests/user`

**Response**

- `200 OK` on success
- `500 Internal Server Error` on server error

```json
{
     "20": {
        "status": "OPEN",
        "labtech_request_id": "62011781",
        "infoType": "uwiIssuedID",
        "newInfo": "67890128",
        "admin_approve_id": "",
    },
    "5": {
        "status": "APPROVED",
        "labtech_request_id": "62011781",
        "infoType": "uwiIssuedID",
        "newInfo": "67890128",
        "admin_approve_id": "6000000",
    },
    "43": {
        "status": "DENIED",
        "labtech_request_id": "60001020",
        "infoType": "lastname",
        "newInfo": "charles",
        "admin_approve_id": "6000000",
    }
}
```

## Admin Approval of request

**Definitions**

`PATCH /web/request/swap/approve`

**Arguments**

- "user_request_id": 5
- "approval_status": "DENIED" or "APPROVED"

**Response**

- `200 OK` on success
- `500 Internal Server Error` issues arise on server
- `400 Bad Request` improper request parameters

**Success**
```json
{
    "message": "Request Updated"
    "status": "APPROVED" / "DENIED"
}
```

**Error**
```json
{
    "message": "Request could not be Updated"
}
```
