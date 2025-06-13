import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base

class ApplicationStatus(enum.Enum):
    """Enumeration for the status of a job application."""
    PENDING = "pending"
    REVIEWED = "reviewed"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class JobApplication(Base):
    """
    SQLAlchemy model for a Job Application.
    Represents a candidate's application for a specific job posting.
    """
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    candidate_profile_id = Column(Integer, ForeignKey("candidate_profiles.id"), nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    cover_letter = Column(Text, nullable=False)
    years_of_experience = Column(String(50), nullable=True) 
    expected_salary = Column(String(100), nullable=True) 
    resume_url = Column(String(512), nullable=True) 
    
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING, nullable=False)
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    job_posting = relationship("JobPosting", back_populates="applications")
    candidate = relationship("CandidateProfile", back_populates="applications")

