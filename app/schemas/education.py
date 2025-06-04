from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

class EducationBase(BaseModel):
    """Base schema for Education data."""
    degree: str
    institution: str
    field_of_study: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class EducationCreate(EducationBase):
    """Schema for creating an Education entry."""
    pass

class EducationUpdate(EducationBase):
    """Schema for updating an Education entry."""
    degree: Optional[str] = None
    institution: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None

class EducationData(EducationBase):
    """Schema for returning Education data, including DB-generated fields."""
    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class EducationRead(EducationData):
    """Full read schema for a single Education entry."""
    pass
