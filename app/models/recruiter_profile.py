from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.user import User 


class RecruiterProfile(Base):
    __tablename__ = "recruiter_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    company_name = Column(String, index=True, nullable=False)
    job_title = Column(String, index=True)
    phone_number = Column(String) 
    linkedin_profile_url = Column(String) 
    website_url = Column(String) 
    bio = Column(Text) 

    location = Column(String, index=True, nullable=True) 
    company_size = Column(String, nullable=True) 
    industry = Column(String, index=True, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship("User", back_populates="recruiter_profile", uselist=False)


    def __repr__(self):
        return f"<RecruiterProfile(id={self.id}, user_id={self.user_id}, company='{self.company_name}')>"

if not hasattr(User, 'recruiter_profile'):
    User.recruiter_profile = relationship("RecruiterProfile", back_populates="user", uselist=False)

