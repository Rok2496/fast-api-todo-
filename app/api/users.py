from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import crud
from ..db.database import SessionLocal
from ..db.models import User
from ..schemas import schemas
from ..api.deps import get_current_user, get_db

router = APIRouter()

@router.get("/me", response_model=schemas.UserProfile)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile with Google connection status."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "two_factor_enabled": current_user.two_factor_enabled,
        "google_connected": current_user.google_refresh_token is not None,
        "created_at": current_user.created_at
    }

@router.post("/google/disconnect", response_model=schemas.SuccessResponse)
def disconnect_google(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Disconnect Google Calendar integration for the current user."""
    if not current_user.google_refresh_token:
        raise HTTPException(status_code=400, detail="Google Calendar not connected")
    
    current_user.google_refresh_token = None
    db.commit()
    db.refresh(current_user)
    
    return {"success": True, "message": "Google Calendar disconnected successfully"} 