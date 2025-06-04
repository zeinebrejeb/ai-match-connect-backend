from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
class CandidateSkillBase(BaseModel):
    """Base schema for Candidate Skill data."""
    name: str
    proficiency: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CandidateSkillCreate(CandidateSkillBase):
    """Schema for creating a Candidate Skill."""
    pass

class CandidateSkillUpdate(CandidateSkillBase):
    """Schema for updating a Candidate Skill."""
    name: Optional[str] = None
    proficiency: Optional[str] = None

class CandidateSkillRead(CandidateSkillBase):
    """Schema for reading/returning a Candidate Skill, including DB-generated fields."""
    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
