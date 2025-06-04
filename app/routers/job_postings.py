from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db 
from app.schemas.job_posting import JobPostingCreate, JobPostingRead, JobPostingUpdate
from app.crud.crud_job_posting import job_posting as crud_job_posting 
from app.crud.crud_job_posting import skills_string_to_list 
from app.models.recruiter_profile import RecruiterProfile 
from app.dependencies.deps import get_current_active_recruiter 

router = APIRouter()

def enrich_job_posting_read(db_job_posting: Any) -> JobPostingRead:
    """
    Helper function to convert stored skills string to list for JobPostingRead schema.
    """
    job_posting_data = db_job_posting.__dict__
    job_posting_data["skills"] = skills_string_to_list(db_job_posting.required_skills)
    return JobPostingRead.model_validate(job_posting_data)


@router.post(
    "/",
    response_model=JobPostingRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Job Posting",
    description="Creates a new job posting linked to the authenticated recruiter's profile.",
)
async def create_job_posting(
    *,
    db: AsyncSession = Depends(get_db),
    job_posting_in: JobPostingCreate,
    current_recruiter: RecruiterProfile = Depends(get_current_active_recruiter),
) -> JobPostingRead:
    """
    Create a new job posting.

    - **job_posting_in**: Job posting data to create.
    - Requires authentication as an active recruiter.
    """
    if not current_recruiter: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recruiter profile not found or not authorized.",
        )
    
    recruiter_profile_id = current_recruiter.id

    created_job = await crud_job_posting.create_with_recruiter_profile(
        db=db, obj_in=job_posting_in, recruiter_profile_id=recruiter_profile_id
    )
    return enrich_job_posting_read(created_job)


@router.get(
    "/{job_posting_id}",
    response_model=JobPostingRead,
    summary="Get a specific Job Posting by ID",
    description="Retrieves details of a specific job posting by its ID.",
)
async def read_job_posting(
    *,
    db: AsyncSession = Depends(get_db),
    job_posting_id: int,

) -> JobPostingRead:
    """
    Get a job posting by ID.
    """
    db_job_posting = await crud_job_posting.get(db=db, id=job_posting_id)
    if not db_job_posting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found"
        )
    return enrich_job_posting_read(db_job_posting)


@router.get(
    "/",
    response_model=List[JobPostingRead],
    summary="Get all Job Postings",
    description="Retrieves a list of all job postings, with pagination.",
)
async def read_job_postings(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    
) -> List[JobPostingRead]:
    """
    Retrieve all job postings with pagination.
    """
    db_job_postings = await crud_job_posting.get_multi(db=db, skip=skip, limit=limit)
    return [enrich_job_posting_read(jp) for jp in db_job_postings]


@router.get(
    "/by-recruiter/me", 
    response_model=List[JobPostingRead],
    summary="Get Job Postings by the current authenticated Recruiter",
    description="Retrieves a list of job postings created by the currently authenticated recruiter.",
)
async def read_job_postings_by_current_recruiter(
    *,
    db: AsyncSession = Depends(get_db),
    current_recruiter: RecruiterProfile = Depends(get_current_active_recruiter),
    skip: int = 0,
    limit: int = 100,
) -> List[JobPostingRead]:
    """
    Retrieve job postings for the currently authenticated recruiter.
    """
    if not current_recruiter:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recruiter profile not found or not authorized.",
        )
    
    recruiter_profile_id = current_recruiter.id
    db_job_postings = await crud_job_posting.get_by_recruiter_profile_id(
        db=db, recruiter_profile_id=recruiter_profile_id, skip=skip, limit=limit
    )
    return [enrich_job_posting_read(jp) for jp in db_job_postings]


@router.put(
    "/{job_posting_id}",
    response_model=JobPostingRead,
    summary="Update a Job Posting",
    description="Updates an existing job posting. Only the recruiter who created it can update.",
)
async def update_job_posting(
    *,
    db: AsyncSession = Depends(get_db),
    job_posting_id: int,
    job_posting_in: JobPostingUpdate,
    current_recruiter: RecruiterProfile = Depends(get_current_active_recruiter),
) -> JobPostingRead:
    """
    Update a job posting.

    - Only the recruiter who created the job posting can update it.
    """
    db_job_posting = await crud_job_posting.get(db=db, id=job_posting_id)
    if not db_job_posting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found"
        )
    if db_job_posting.recruiter_profile_id != current_recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job posting",
        )

    updated_job_posting = await crud_job_posting.update(
        db=db, db_obj=db_job_posting, obj_in=job_posting_in
    )
    return enrich_job_posting_read(updated_job_posting)


@router.delete(
    "/{job_posting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Job Posting",
    description="Deletes a job posting. Only the recruiter who created it can delete.",
)
async def delete_job_posting(
    *,
    db: AsyncSession = Depends(get_db),
    job_posting_id: int,
    current_recruiter: RecruiterProfile = Depends(get_current_active_recruiter),
) -> None:
    """
    Delete a job posting.

    - Only the recruiter who created the job posting can delete it.
    - Returns 204 No Content on successful deletion.
    """
    db_job_posting = await crud_job_posting.get(db=db, id=job_posting_id)
    if not db_job_posting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found"
        )
    if db_job_posting.recruiter_profile_id != current_recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job posting",
        )

    await crud_job_posting.remove(db=db, id=job_posting_id)
    return None 

