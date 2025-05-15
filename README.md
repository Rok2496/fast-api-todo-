# FAST TODO API

A powerful task management API with secure authentication, two-factor security, and Google Calendar integration.

## Features

- **Secure Authentication**
  - JWT-based authentication
  - Password hashing
  - Two-factor authentication (2FA)
  - One-time login codes

- **Todo Management**
  - Create, read, update, delete (CRUD) operations
  - Due date tracking
  - Completion status

- **Google Calendar Integration**
  - Connect with Google OAuth
  - Add todos to Google Calendar
  - Manage calendar integration

## Project Structure

```
fast/
├── app/                     # Main application package
│   ├── api/                 # API endpoints
│   │   ├── auth.py          # Authentication routes
│   │   ├── deps.py          # Dependencies
│   │   ├── google.py        # Google OAuth integration
│   │   ├── todo.py          # Todo CRUD operations
│   │   └── users.py         # User profile management
│   │
│   ├── core/                # Core functionality
│   │   ├── auth.py          # Authentication utilities
│   │   └── utils.py         # Utility functions
│   │
│   ├── db/                  # Database
│   │   ├── crud.py          # Database operations
│   │   ├── database.py      # Database connection
│   │   └── models.py        # SQLAlchemy models
│   │
│   ├── schemas/             # Pydantic schemas
│   │   └── schemas.py       # Data validation models
│   │
│   ├── services/            # External services
│   │   └── google_calendar.py  # Google Calendar API
│   │
│   └── main.py              # FastAPI application entry point
│
├── scripts/                 # Utility scripts
│   ├── create_tables.py     # Create database tables
│   ├── init_db.py           # Initialize database
│   ├── migrate_add_otp_code.py  # Migration script
│   └── setup_db.py          # Database setup
│
├── .env                     # Environment variables (not in git)
├── .gitignore               # Git ignore file
├── requirements.txt         # Python dependencies
└── setup.py                 # Package setup
```

## API Endpoints

### Authentication

- **POST /auth/register**: Register a new user
- **POST /auth/login**: Login to get access token
- **POST /auth/2fa/setup**: Set up two-factor authentication
- **POST /auth/2fa/verify**: Verify 2FA code
- **POST /auth/onetime/request**: Request one-time login code
- **POST /auth/onetime/verify**: Verify one-time login code

### Todo Management

- **GET /todos**: Get all todos for the current user
- **POST /todos**: Create a new todo
- **GET /todos/{todo_id}**: Get a specific todo
- **PUT /todos/{todo_id}**: Update a todo
- **DELETE /todos/{todo_id}**: Delete a todo
- **POST /todos/calendar/add**: Add todo to Google Calendar

### User Profile

- **GET /users/me**: Get current user profile
- **POST /users/google/disconnect**: Disconnect Google Calendar

### Google Integration

- **GET /auth/google/authorize**: Start Google OAuth flow
- **GET /auth/google/callback**: Handle Google OAuth callback

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Google API credentials (for Calendar integration)

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost/tododb
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
FRONTEND_REDIRECT_URL=http://localhost:3000/settings
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASS=password
FROM_EMAIL=noreply@example.com
```

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database setup script:
   ```bash
   python scripts/setup_db.py
   ```
5. Run migrations:
   ```bash
   python scripts/migrate_add_otp_code.py
   ```
6. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 