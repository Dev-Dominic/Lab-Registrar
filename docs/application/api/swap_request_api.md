# Requests

Details API endpoints for SwapRequests

## Get a request

**Definitions**

`GET /web/request/all`

**Response**

- `200 OK` on success

**OPEN Request**

```json
{
     "10":{
        "status": "OPEN",
        "labtech_request_id": "62011781",
        "labtech_confirm_id": "",
        "admin_approve": "",
        "request_labtech_timeslot_id": 5,
        "confirm_timeslot_id": ""
    }
}
```

**CONFIRM Request**

```json
{
     "10":{
        "status": "CONFIRM",
        "labtech_request_id": "62011781",
        "labtech_confirm_id": "60000007",
        "admin_approve": "",
        "request_labtech_timeslot_id": 5,
        "confirm_timeslot_id": 20
    }
}
```

**APPROVE Request**

```json
{
     "10":{
        "status": "APPROVED",
        "labtech_request_id": "62011781",
        "labtech_confirm_id": "60000007",
        "admin_approve": "6000000",
        "request_labtech_timeslot_id": 5,
        "confirm_timeslot_id": 20
    }
}
```

## Post a request

**Definitions**

`POST /web/request/swap`

**Arguments**

- "request_labtech_timeslot_id" : 5

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

## Get all requests

**Definitions**

`GET /web/requests/swap`

**Response**

- `200 OK` on success

```json
{
     "20": {
        "status": "OPEN",
        "labtech_request_id": "62011781",
        "labtech_confirm_id": "",
        "admin_approve": "",
        "request_labtech_timeslot_id": 5,
        "confirm_timeslot_id": ""
    },
    "5": {
        "status": "CONFIRM",
        "labtech_request_id": "62011781",
        "labtech_confirm_id": "61981091",
        "admin_approve": "",
        "request_labtech_timeslot_id": 5,
        "confirm_timeslot_id": 18
    }
}
```

## Update swap request with another labtech acceptance

**Definitions**

`PATCH /web/request/swap/accept`

**Arguments**

- "swap_request_id": 5
- "confirm_timeslot_id": 18

**Response**

- `200 OK` on success
- `500 Internal Server Error` issues arise on server
- `400 Bad Request` improper request parameters

**Success**
```json
{
    "message": "Counter offer made"
}
```

**Error**
```json
{
    "message": "Counter offer was not made"
}
```


## Admin Approval of request

**Definitions**

`PATCH /web/request/swap/accept`

**Arguments**

- "swap_request_id": 5
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

**Success**
```json
{
    "message": "Request could not be Updated"
}
```
