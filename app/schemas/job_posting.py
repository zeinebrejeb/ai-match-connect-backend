from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.job_posting import JobType, ExperienceLevel

class JobPostingBase(BaseModel):
    """Base schema for Job Posting data."""
    title: str
    location: str
    type: JobType 
    experience_level: ExperienceLevel 
    salary_range: Optional[str] = None
    description: str

    model_config = ConfigDict(from_attributes=True)

class JobPostingCreate(JobPostingBase):
    """Schema for creating a Job Posting."""

    skills: List[str] = [] 

class JobPostingUpdate(JobPostingBase):
    """Schema for updating a Job Posting."""
    title: Optional[str] = None 
    location: Optional[str] = None
    type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    salary_range: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None  

class JobPostingRead(JobPostingBase):
    """Schema for reading/returning a Job Posting."""
    id: int 
    recruiter_profile_id: int 
    created_at: datetime
    updated_at: datetime
    skills: List[str] = []
    
class JobPostingListResponse(BaseModel):
    items: List[JobPostingRead]
    total: int
    page: Optional[int] = None 
    size: Optional[int] = None