from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    completed: Optional[bool] = None

class TodoOut(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    two_factor_enabled: bool
    created_at: datetime
    class Config:
        orm_mode = True
        from_attributes = True

class UserProfile(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    two_factor_enabled: bool
    google_connected: bool
    created_at: datetime
    class Config:
        orm_mode = True
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class TwoFactorVerify(BaseModel):
    otp: str

class OneTimeLoginRequest(BaseModel):
    email: EmailStr

class OneTimeLoginVerify(BaseModel):
    email: EmailStr
    code: str

class SuccessResponse(BaseModel):
    success: bool
    message: str = "Operation completed successfully" 