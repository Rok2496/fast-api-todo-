# API Documentation

## Authentication Endpoints

### Register a new user

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "is_verified": false,
  "two_factor_enabled": false,
  "created_at": "2023-06-01T12:00:00"
}
```

### Login

**Endpoint:** `POST /auth/login`

**Request Body (form data):**
```
username=user@example.com
password=securepassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Setup Two-Factor Authentication

**Endpoint:** `POST /auth/2fa/setup`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "otp_uri": "otpauth://totp/TodoApp:user@example.com?secret=ABCDEFGHIJKLMNOP&issuer=TodoApp"
}
```

### Verify Two-Factor Authentication

**Endpoint:** `POST /auth/2fa/verify`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "otp": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Request One-Time Login Code

**Endpoint:** `POST /auth/onetime/request`

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "msg": "One-time login code sent to your email"
}
```

### Verify One-Time Login Code

**Endpoint:** `POST /auth/onetime/verify`

**Request Body:**
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Todo Endpoints

### Get All Todos

**Endpoint:** `GET /todos`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the MVP by Friday",
    "due_date": "2023-06-15T17:00:00",
    "completed": false,
    "created_at": "2023-06-01T12:00:00",
    "updated_at": "2023-06-01T12:00:00"
  }
]
```

### Create a Todo

**Endpoint:** `POST /todos`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Complete project",
  "description": "Finish the MVP by Friday",
  "due_date": "2023-06-15T17:00:00"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the MVP by Friday",
  "due_date": "2023-06-15T17:00:00",
  "completed": false,
  "created_at": "2023-06-01T12:00:00",
  "updated_at": "2023-06-01T12:00:00"
}
```

### Get a Todo

**Endpoint:** `GET /todos/{todo_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the MVP by Friday",
  "due_date": "2023-06-15T17:00:00",
  "completed": false,
  "created_at": "2023-06-01T12:00:00",
  "updated_at": "2023-06-01T12:00:00"
}
```

### Update a Todo

**Endpoint:** `PUT /todos/{todo_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Complete project",
  "description": "Updated description",
  "due_date": "2023-06-15T17:00:00",
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Updated description",
  "due_date": "2023-06-15T17:00:00",
  "completed": true,
  "created_at": "2023-06-01T12:00:00",
  "updated_at": "2023-06-01T13:00:00"
}
```

### Delete a Todo

**Endpoint:** `DELETE /todos/{todo_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "msg": "Todo deleted"
}
```

### Add Todo to Google Calendar

**Endpoint:** `POST /todos/calendar/add`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "todo_id": 1
}
```

**Response:**
```json
{
  "event_id": "google_event_id_12345"
}
```

## User Endpoints

### Get Current User Profile

**Endpoint:** `GET /users/me`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "is_verified": true,
  "two_factor_enabled": true,
  "google_connected": true,
  "created_at": "2023-06-01T12:00:00"
}
```

### Disconnect Google Calendar

**Endpoint:** `POST /users/google/disconnect`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Google Calendar disconnected successfully"
}
```

## Google OAuth Endpoints

### Get Google Authorization URL

**Endpoint:** `GET /auth/google/authorize`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/auth?..."
}
```

### Google OAuth Callback

**Endpoint:** `GET /auth/google/callback`

**Query Parameters:**
```
code=<authorization_code>
state=<user_id>
```

**Redirects to:** `<FRONTEND_REDIRECT_URL>?google_connected=true&access_token=<new_token>` 