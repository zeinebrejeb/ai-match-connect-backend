from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.schemas.experience import ExperienceData
from app.schemas.education import EducationData
from app.schemas.skill import CandidateSkillBase

class CandidateProfileBase(BaseModel):
    """Base schema for Candidate Profile data."""
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    resume_url: Optional[str] = None 

    model_config = ConfigDict(from_attributes=True)


class CandidateProfileCreate(CandidateProfileBase):
    """Schema for creating a Candidate Profile."""
    pass


class CandidateProfileUpdate(CandidateProfileBase):
    """Schema for updating a Candidate Profile."""
    pass

class CandidateProfileRead(CandidateProfileBase):
    """
    Schema for reading/returning a Candidate Profile,
    including related User data and nested experiences, educations, and skills.
    """
    id: int 
    user_id: int # Foreign key 
    created_at: datetime
    updated_at: datetime
    email: EmailStr
    is_active: bool
    role: str
    first_name: Optional[str] = None 
    last_name: Optional[str] = None  
    experiences: List[ExperienceData] = []
    educations: List[EducationData] = []
    skills: List[CandidateSkillBase] = []

