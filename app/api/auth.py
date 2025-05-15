from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from ..db import crud
from ..db.database import SessionLocal
from ..db.models import User
from ..schemas import schemas
from ..core import auth, utils
from ..api.deps import get_current_user, get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if user.two_factor_enabled:
        # 2FA required
        raise HTTPException(status_code=403, detail="2FA required")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/2fa/setup")
def setup_2fa(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.two_factor_enabled:
        raise HTTPException(status_code=400, detail="2FA already enabled")
    secret = auth.generate_2fa_secret()
    uri = auth.get_totp_uri(secret, current_user.email)
    crud.enable_2fa(db, current_user, secret)
    return {"otp_uri": uri}

@router.post("/2fa/verify")
def verify_2fa(data: schemas.TwoFactorVerify, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.two_factor_enabled:
        raise HTTPException(status_code=400, detail="2FA not enabled")
    if not crud.verify_2fa(db, current_user, data.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    access_token = auth.create_access_token(data={"sub": current_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/onetime/request")
async def request_one_time_login(data: schemas.OneTimeLoginRequest, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    user = crud.get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate a one-time numeric code
    code = auth.generate_one_time_code()
    
    # Store the code in the database with expiry
    crud.set_one_time_code(db, user, code)
    
    # Send the code via email
    subject = "Your One-Time Login Code"
    body = f"Your one-time login code is: {code}\n\nThis code will expire in 10 minutes."
    
    if background_tasks:
        background_tasks.add_task(utils.send_email_async, user.email, subject, body)
    else:
        await utils.send_email_async(user.email, subject, body)
    
    return {"msg": "One-time login code sent to your email"}

@router.post("/onetime/verify", response_model=schemas.Token)
def verify_one_time_login(data: schemas.OneTimeLoginVerify, db: Session = Depends(get_db)):
    user = crud.verify_one_time_code(db, data.email, data.code)
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"} 