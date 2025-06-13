from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.schemas.job_application import JobApplicationCreate, JobApplicationRead
from app.crud.crud_job_application import job_application as crud_job_application
from app.models.candidate_profile import CandidateProfile
from app.dependencies.deps import get_current_active_candidate

router = APIRouter(prefix="/job-applications", tags=["Job Applications"])

@router.post(
    "/",
    response_model=JobApplicationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new Job Application",
    description="Allows an authenticated candidate to submit an application for a job posting.",
)
async def submit_job_application(
    *,
    db: AsyncSession = Depends(get_db),
    application_in: JobApplicationCreate,
    current_candidate: CandidateProfile = Depends(get_current_active_candidate),
) -> JobApplicationRead:
    """
    Endpoint to submit a job application.
    The application is automatically linked to the currently authenticated candidate's profile.
    """
    if not current_candidate:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Candidate profile not found or not authorized.",
        )
    
    # Check if the candidate has already applied for this job
    # existing_applications = await crud_job_application.get_multi_by_candidate_and_job(...)
    # if existing_applications:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="You have already applied for this job.",
    #     )

    created_application = await crud_job_application.create_with_candidate(
        db=db, obj_in=application_in, candidate_profile_id=current_candidate.id
    )
    return created_application

@router.get(
    "/my-applications",
    response_model=List[JobApplicationRead],
    summary="Get all applications for the current candidate",
)
async def get_my_applications(
    db: AsyncSession = Depends(get_db),
    current_candidate: CandidateProfile = Depends(get_current_active_candidate),
    skip: int = 0,
    limit: int = 100,
) -> List[JobApplicationRead]:
    """
    Retrieves all job applications submitted by the currently authenticated candidate.
    """
    applications = await crud_job_application.get_multi_by_candidate(
        db=db, candidate_profile_id=current_candidate.id, skip=skip, limit=limit
    )
    return applications
