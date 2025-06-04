from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class CandidateJobMatch(BaseModel):
    id: int
    title: str
    company: str
    location: str
    posted_date: str
    salary: Optional[str] = None
    skills: List[str] = []
    match_reasons: List[str] = [] 


class RecruiterCandidateMatch(BaseModel):
    id: int 
    name: str 
    avatar: Optional[str] = None 
    title: Optional[str] = None 
    location: Optional[str] = None
    experience: Optional[str] = None 
    skills: List[str] = []
    match_reasons: List[str] = [] 


class RecentActivityItem(BaseModel):
    id: int
    type: str  
    message: str
    timestamp: str

    
    model_config = {"from_attributes": True}


class RecruiterDashboardData(BaseModel):
    """Schema for the Recruiter Dashboard data."""
    user_name: str 
    profile_completeness_percentage: int 
    total_active_jobs: int
    total_applicants: int 
    total_ai_matched_candidates: int 
    top_candidate_matches: List[RecruiterCandidateMatch] 
    recent_activity: List[RecentActivityItem] 

class RecruiterCandidateMatch(BaseModel):
    id: int 
    name: str
    avatar: Optional[HttpUrl] = None 
    title: str 
    location: Optional[str] = None
    experience: Optional[str] = None 
    skills: List[str] = []
    match_reasons: List[str] = []
    match_score: Optional[int] = None 

    model_config = {"from_attributes": True}


class RecruiterDashboardData(BaseModel):
    user_name: str
    profile_completeness_percentage: int
    total_active_jobs: int
    total_applicants: int
    total_ai_matched_candidates: int
    top_candidate_matches: List[RecruiterCandidateMatch] = []
    recent_activity: List[RecentActivityItem] = []

    model_config = {"from_attributes": True}


