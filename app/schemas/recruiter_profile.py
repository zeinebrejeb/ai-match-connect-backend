from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.user import UserRole 
class RecruiterProfileBase(BaseModel):
    """Base schema for Recruiter Profile data."""
    company_name: str
    job_title: Optional[str] = None
    phone_number: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    website_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None 
    company_size: Optional[str] = None 
    industry: Optional[str] = None

    # Configuration for ORM mode (allows creating Pydantic model from SQLAlchemy instance)
    model_config = ConfigDict(from_attributes=True)

class RecruiterProfileCreate(RecruiterProfileBase):
    """Schema for creating a Recruiter Profile."""

class RecruiterProfileUpdate(RecruiterProfileBase):
    """Schema for updating a Recruiter Profile."""
    company_name: Optional[str] = None

class RecruiterProfileRead(RecruiterProfileBase):
    """Schema for reading/returning a Recruiter Profile, including related User data."""
    id: int 
    user_id: int 
    created_at: datetime
    updated_at: datetime
    first_name: Optional[str] = None 
    last_name: Optional[str] = None 
    email: EmailStr 
    is_active: bool 
    role: UserRole 
    model_config = ConfigDict(from_attributes=True) 

