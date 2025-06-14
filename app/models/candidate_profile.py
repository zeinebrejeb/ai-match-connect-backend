from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.user import User 
from sqlalchemy.orm import Mapped, mapped_column

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    phone_number = Column(String, nullable=True)
    location = Column(String, nullable=True)
    linkedin_profile_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    resume_text: Mapped[str] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="candidate_profile", uselist=False)
    experiences = relationship("Experience", back_populates="candidate_profile", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="candidate_profile", cascade="all, delete-orphan")
    candidate_skills = relationship("CandidateSkill", back_populates="candidate_profile", cascade="all, delete-orphan")

    applications = relationship(
        "JobApplication", 
        back_populates="candidate_profile", 
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<CandidateProfile(id={self.id}, user_id={self.user_id})>"
