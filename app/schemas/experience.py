from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

class ExperienceBase(BaseModel):
    """Base schema for Experience data."""
    title: str
    company: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ExperienceCreate(ExperienceBase):
    """Schema for creating an Experience entry."""
    pass

class ExperienceUpdate(ExperienceBase):
    """Schema for updating an Experience entry."""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None


class ExperienceData(ExperienceBase):
    """Schema for returning Experience data, including DB-generated fields."""
    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ExperienceRead(ExperienceData):
    """Full read schema for a single Experience entry."""
    pass
