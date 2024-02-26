# Project Setup 

## Requirement
Docker

```
docker-compose build
docker-compose up
```
## Base URL

local

http://127.0.0.1:8080


# API Documentation

This documentation provides information about the  API .

## Signup API

### Endpoint

`POST /api/auth/signup/`

### Request Body

```json
{
  "name": "example",
  "email": "example@examplel.com",
  "password": "secure_password123",
  "dob": "1990-01-01"
}
```
Success Response
```json
{
    "data": {
        "refresh": "",
        "access": ""
    },
    "success": true,
    "message": "account creation successful"
}
```
Error Response
```json
{
    "errors": {
        "field_name": ["error_message"],
        "another_field": ["error_message"]
    },
    "success": false,
    "message": "Error message"
}
```
Notes
The name and email fields should be unique.
Password must meet the security requirements.
The dob (Date of Birth) field is optional.


## Login API

### Endpoint

`POST /api/auth/login/`

### Request Body

```json
{
  "email": "example@examplel.com",
  "password": "secure_password123"
}
```
Success Response
```json
{
    "data": {
        "refresh": "",
        "access": ""
    },
    "success": true,
    "message": "Login successful"
}
```
Error Response
```json
{
    "errors": {
        "error": ["Invalid credentials"]
    },
    "success": false,
    "message": "Error"
}
```
Notes
The email and password fields are required for login.
Ensure that the provided credentials are correct for successful login.


## Refresh Token API

### Endpoint

`POST /api/auth/refresh-token/`

### Request Body

```json
{
    "refresh_token": "your_refresh_token_here"
}
```
Success Response
```json
{
    "data": {
        "access_token": "your_new_access_token_here",
        "refresh_token": "your_new_refresh_token_here"
    },
    "success": true,
    "message": "Token refreshed successfully"
}
```
Error Response
```json
{
    "errors": {
        "error": ["Invalid refresh token"]
    },
    "success": false,
    "message": "Error"
}
```
Notes
Provide a valid refresh_token for refreshing the access token.
The refresh_token is obtained during the login process.
Ensure that the provided refresh token is valid for a successful refresh.



# Note API

## Create/Update Note  API

### Endpoint

`POST /api/notes/createnote/`

### Request Headers

Authorization: Bearer Token (Include your valid access token)


### Request Body

```json
{
   "noteId": "",
   "content": {
        "ops": [
            { "insert": "Hello, " },
            { "insert": "world", "attributes": { "bold": true } },
            { "insert": "!" }
        ]
},
    "title": "new Notes 2 "
}
```
Success Response
```json
{
    
    "success": true,
    "message": "Note updated/Created successfully"
}
```
Error Response
```json
{
    "errors": {
        "error": ["Note with the given ID does not exist"]
    },
    "success": false,
    "message": "Error"
}
```
Notes
Provide a valid access toekn for the Request.





## GET  Note  API

### Endpoint

`GET /api/notes/`

### Request Headers

Authorization: Bearer Token (Include your valid access token)


Success Response
```json
{
    "data":{
            "count": "count",
            "next": "next_link",
            "previous": "self.get_previous_link()",
            "results": {}
        },
    "success": true,
    "message": "data successfully retrieved"
}
```
Error Response
```json
{
    "errors": {
        "error": ["error occured"]
    },
    "success": false,
    "message": "Error"
}
```
Notes
Provide a valid access toekn for the Request.



## Delete Note  API

### Endpoint

`DELETE /api/notes/`

### Request Headers

Authorization: Bearer Token (Include your valid access token)


### Request Body

```json
{
   "noteId": "",
}
```
Success Response
```json
{
    
    "success": true,
    "message": "Note deleted successfully"
}
```
Error Response
```json
{
    "errors": {
        "error": ["Note does not exist/Validation Error"]
    },
    "success": false,
    "message": "Error"
}
```
Notes
Provide a valid access toekn for the Request.




## ToggleNotePinStatus Note  API

### Endpoint

`POST /api/notes/togglepin/`

### Request Headers

Authorization: Bearer Token (Include your valid access token)


### Request Body

```json
{
   "noteId": "",
}
```
Success Response
```json
{
    
    "success": true,
    "message": "Note pin status toggled successfully"
}
```
Error Response
```json
{
    "errors": {
        "error": ["Note does not exist/Validation Error"]
    },
    "success": false,
    "message": "Please provide a valid note ID"
}
```
Notes
Provide a valid access toekn for the Request.


