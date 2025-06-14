from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base 
import enum 

class UserRole(str, enum.Enum):
    candidate = "candidate"
    recruiter = "recruiter"
    admin = "admin" 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, index=True) 
    last_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.candidate, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) 
    

    candidate_profile = relationship(
        "CandidateProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    recruiter_profile = relationship(
        "RecruiterProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # uselist=False indique une relation one-to-one du point de vue de User
    # cascade="all, delete-orphan" : si un User est supprimé, son CandidateProfile associé l'est aussi.
    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}')>"