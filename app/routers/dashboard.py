from typing import Any, List, Optional 
import random 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import crud, schemas
from app.models.user import User
from app.models.job_posting import JobPosting 
from app.dependencies import deps
from sqlalchemy import func

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/recruiter", response_model=schemas.RecruiterDashboardData)
async def get_recruiter_dashboard_data(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_recruiter)
) -> Any:
    """
    Get data for the recruiter dashboard for the current authenticated recruiter.
    """
    recruiter_profile = current_user.recruiter_profile
    if not recruiter_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found for this user."
        )


    user_name = f"{current_user.first_name or ''} {current_user.last_name or ''}".strip()
    if not user_name:
        user_name = current_user.email 

    
    statement_count_jobs = select(func.count(JobPosting.id)).where(JobPosting.recruiter_profile_id == recruiter_profile.id)
    total_active_jobs_result = await db.execute(statement_count_jobs)
    total_active_jobs = total_active_jobs_result.scalar_one()


    simulated_profile_completeness = 80 + random.randint(0, 20) 

    simulated_total_applicants = total_active_jobs * random.randint(5, 15)

    simulated_total_ai_matched_candidates = int(simulated_total_applicants * random.uniform(0.3, 0.7))

    simulated_top_candidate_matches: List[schemas.RecruiterCandidateMatch] = [
        schemas.RecruiterCandidateMatch(
            id=101,
            name="Michael Johnson",
            avatar="https://i.pravatar.cc/150?img=68",
            title="Senior Software Engineer",
            location="San Francisco, CA",
            experience="6+ years",
            skills=["Python", "FastAPI", "SQLAlchemy", "Docker"],
            match_reasons=["Strong backend experience", "Matches required skills"]
        ),
        schemas.RecruiterCandidateMatch(
            id=102,
            name="Emma Rodriguez",
            avatar="https://i.pravatar.cc/150?img=69",
            title="Full Stack Developer",
            location="Remote",
            experience="5+ years",
            skills=["React", "Node.js", "MongoDB", "AWS"],
            match_reasons=["Full stack expertise", "Experience with tech stack"]
        ),
        schemas.RecruiterCandidateMatch(
            id=103,
            name="David Chen",
            avatar="https://i.pravatar.cc/150?img=70", 
            title="Frontend Lead",
            location="New York, NY",
            experience="7+ years",
            skills=["React", "TypeScript", "GraphQL", "Leadership"],
            match_reasons=["Leadership experience", "Frontend specialization"]
        ),
    ]


    simulated_recent_activity: List[schemas.RecentActivityItem] = [
        schemas.RecentActivityItem(id=1, type="new_application", message="New application for Senior React Developer", timestamp="1 hour ago"),
        schemas.RecentActivityItem(id=2, type="new_match", message="New high match candidate for Full Stack Engineer", timestamp="Yesterday"),
        schemas.RecentActivityItem(id=3, type="job_view", message="Your Frontend Engineer job listing received 5 views", timestamp="2 days ago"),
    ]

    return schemas.RecruiterDashboardData(
        user_name=user_name,
        profile_completeness_percentage=simulated_profile_completeness,
        total_active_jobs=total_active_jobs,
        total_applicants=simulated_total_applicants,
        total_ai_matched_candidates=simulated_total_ai_matched_candidates,
        top_candidate_matches=simulated_top_candidate_matches,
        recent_activity=simulated_recent_activity,
    )
