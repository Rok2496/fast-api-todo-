from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from ..db import crud
from ..db.database import SessionLocal
from ..db.models import User
from ..schemas import schemas
from ..api.deps import get_current_user, get_db
from ..core.auth import create_access_token

router = APIRouter()

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://fast-api-todo-e9rg.onrender.com/auth/google/callback")
FRONTEND_REDIRECT_URL = os.getenv("FRONTEND_REDIRECT_URL", "https://6825f2bc475882004400bca9--todoregex.netlify.app/settings")

# Define OAuth2 scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
def create_flow():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [GOOGLE_REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    return flow

@router.get("/authorize", response_model=schemas.AuthorizationResponse)
def google_authorize(request: Request, current_user: User = Depends(get_current_user)):
    """Generate authorization URL for Google OAuth."""
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google API credentials not configured")
    
    # Create the flow instance
    flow = create_flow()
    
    # Store user ID in the state parameter
    user_id = str(current_user.id)
    
    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',  # Enable offline access to get a refresh token
        prompt='consent',       # Force showing the consent dialog
        include_granted_scopes='true',  # Enable incremental authorization
        state=user_id  # Pass the user ID in the state parameter
    )
    
    return {"authorization_url": authorization_url}

@router.get("/callback")
async def google_callback(
    response: Response,
    code: str,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Handle the Google OAuth callback without requiring authentication."""
    try:
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
            return RedirectResponse(
                url=f"{FRONTEND_REDIRECT_URL}?error=missing_credentials&google_connected=false"
            )
        
        # Extract user_id from state
        if not state or not state.isdigit():
            return RedirectResponse(
                url=f"{FRONTEND_REDIRECT_URL}?error=invalid_state&google_connected=false"
            )
        
        user_id = int(state)
        
        # Get the user from the database using the user_id
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return RedirectResponse(
                url=f"{FRONTEND_REDIRECT_URL}?error=user_not_found&google_connected=false"
            )
        
        # Create the flow instance
        flow = create_flow()
        
        # Exchange the authorization code for credentials
        flow.fetch_token(code=code)
        
        # Get credentials including the refresh token
        credentials = flow.credentials
        
        # Store the refresh token in the user's record
        user.google_refresh_token = credentials.refresh_token
        db.commit()
        db.refresh(user)
        
        # Generate a new access token for the user
        access_token = create_access_token(data={"sub": user.email})
        
        # Redirect to the frontend with success information
        return RedirectResponse(
            url=f"{FRONTEND_REDIRECT_URL}?google_connected=true&access_token={access_token}"
        )
        
    except Exception as e:
        # Log the error (in a real application)
        print(f"Google OAuth error: {str(e)}")
        
        # Redirect to frontend with error
        return RedirectResponse(
            url=f"{FRONTEND_REDIRECT_URL}?error={str(e)}&google_connected=false"
        ) 