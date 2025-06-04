from typing import List, Optional
from pydantic import BaseModel

class ExperienceData(BaseModel):
    """Schema for extracted experience data."""
    company: str
    position: str
    duration: Optional[str] = None 
class EducationData(BaseModel):
    """Schema for extracted education data."""
    degree: str
    institution: str
    year: Optional[str] = None 


class ExtractedCVData(BaseModel):
    """Schema for the complete data extracted from a CV."""
    skills: List[str] = [] 
    experiences: List[ExperienceData] = [] 
    education: List[EducationData] = [] 


class CVAnalysisResponse(BaseModel):
    """Schema for the response containing extracted CV data."""
    extractedData: ExtractedCVData 
    message: str = "CV analyzed successfully." 

