from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.schemas.candidate_profile import CandidateProfileRead
from app.schemas.recruiter_profile import RecruiterProfileRead

class UserBase(BaseModel):
    """Base schema for User data."""
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    """Schema for creating a new User."""
    password: str 
    role: str 

class UserUpdate(UserBase):
    """Schema for updating an existing User."""
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    role: Optional[str] = None 

class User(UserBase):
    """Schema for returning User data, including DB-generated fields and relationships."""
    id: int
    is_active: bool
    is_superuser: bool
    role: str
    created_at: datetime
    updated_at: datetime
    candidate_profile: Optional[CandidateProfileRead] = None
    recruiter_profile: Optional[RecruiterProfileRead] = None 
    model_config = ConfigDict(from_attributes=True)


# This schema is used for returning user data, including DB-generated fields
# and potentially nested relationships