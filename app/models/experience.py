from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date, func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    candidate_profile_id = Column(Integer, ForeignKey("candidate_profiles.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True) 
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    candidate_profile = relationship("CandidateProfile", back_populates="experiences")