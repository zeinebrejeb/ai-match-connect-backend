import enum 
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base 
from app.models.recruiter_profile import RecruiterProfile 

class JobType(str, enum.Enum):
    """Enum for job types."""
    full_time = "full-time"
    part_time = "part-time"
    contract = "contract"
    freelance = "freelance"
    internship = "internship"

class ExperienceLevel(str, enum.Enum):
    """Enum for experience levels."""
    entry = "entry"
    mid = "mid"
    senior = "senior"
    lead = "lead"
    executive = "executive"


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_profile_id = Column(Integer, ForeignKey("recruiter_profiles.id"), nullable=False)

    title = Column(String, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    type = Column(Enum(JobType), nullable=False) 
    experience_level = Column(Enum(ExperienceLevel), nullable=False) 
    salary_range = Column(String, nullable=True) 
    description = Column(Text, nullable=False)

    required_skills = Column(Text, nullable=True) # Store skills as text 

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Define the relationship back to the RecruiterProfile model
    recruiter_profile = relationship("RecruiterProfile", back_populates="job_postings")


    def __repr__(self):
        return f"<JobPosting(id={self.id}, title='{self.title}', recruiter_profile_id={self.recruiter_profile_id})>"

if not hasattr(RecruiterProfile, 'job_postings'):
    RecruiterProfile.job_postings = relationship("JobPosting", back_populates="recruiter_profile")

