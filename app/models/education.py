from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date, func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    candidate_profile_id = Column(Integer, ForeignKey("candidate_profiles.id"), nullable=False, index=True)
    institution_name = Column(String, nullable=False)
    degree = Column(String, nullable=True) 
    field_of_study = Column(String, nullable=True) 
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True) 
    description = Column(Text, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    candidate_profile = relationship("CandidateProfile", back_populates="educations")