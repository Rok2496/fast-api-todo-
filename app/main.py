"""
FAST TODO API - Main Application

This is the main entry point for the FastAPI application.
It initializes the database, sets up middleware, and includes all API routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine
from .db import models
from .api import auth, todo, users, google

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="API for Todo application with authentication and Google Calendar integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                                  # Local development
        "https://6825f2bc475882004400bca9--todoregex.netlify.app", # Deployed frontend
        "*"                                                        # For development only, remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(todo.router, prefix="/todos", tags=["Todo Items"])
app.include_router(users.router, prefix="/users", tags=["User Profile"])
app.include_router(google.router, prefix="/auth/google", tags=["Google Integration"])

@app.get("/")
def read_root():
    """Return basic API information."""
    return {
        "message": "Welcome to the Todo API",
        "docs": "/docs",
        "version": "1.0.0"
    } 