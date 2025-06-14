from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from app.models.job_application import ApplicationStatus
from app.schemas.job_posting import JobPostingRead 
from app.schemas.candidate_profile import CandidateProfileRead

class JobApplicationBase(BaseModel):
    """Base Pydantic schema for job application data."""
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    cover_letter: str
    years_of_experience: Optional[str] = None
    expected_salary: Optional[str] = None
    resume_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class JobApplicationCreate(JobApplicationBase):
    """Schema for creating a new Job Application."""
    job_posting_id: int

class JobApplicationUpdate(BaseModel):
    """Schema for updating a job application's status."""
    status: ApplicationStatus


class JobApplicationRead(JobApplicationBase):
    """Schema for reading/returning a Job Application from the API."""
    id: int
    job_posting_id: int
    candidate_profile_id: int
    status: ApplicationStatus
    applied_at: datetime


class JobApplicationReadDetailed(JobApplicationRead):
    """
    Schema for reading a single, detailed Job Application, including the
    nested job posting and candidate profile information.
    """
    job_posting: JobPostingRead
    candidate: CandidateProfileRead
