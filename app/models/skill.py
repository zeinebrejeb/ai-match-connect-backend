from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.candidate_profile import CandidateProfile 

class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    id = Column(Integer, primary_key=True, index=True)
    candidate_profile_id = Column(Integer, ForeignKey("candidate_profiles.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    proficiency = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    candidate_profile = relationship("CandidateProfile", back_populates="candidate_skills")

    def __repr__(self):
        return f"<CandidateSkill(id={self.id}, name='{self.name}', candidate_profile_id={self.candidate_profile_id})>"

