from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas

from app.models.user import User
from app.dependencies import deps

router = APIRouter(
    prefix="/recruiter-profiles",
    tags=["recruiter-profiles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.RecruiterProfileRead, status_code=status.HTTP_201_CREATED)
async def create_recruiter_profile_for_current_user(
    profile_in: schemas.RecruiterProfileCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_recruiter)
) -> Any:
    """
    Create a recruiter profile for the current authenticated recruiter user.
    A recruiter user can only have one profile.
    """
    if current_user.recruiter_profile:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a recruiter profile."
        )

    profile = await crud.recruiter_profile.create_with_owner( 
        db=db,
        user_id=current_user.id,
        obj_in=profile_in
    )

    return schemas.RecruiterProfileRead(
        id=profile.id,
        user_id=profile.user_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        company_name=profile.company_name,
        job_title=profile.job_title,
        location=profile.location,
        phone_number=profile.phone_number,
        website_url=profile.website_url,
        linkedin_profile_url=profile.linkedin_profile_url,
        bio=profile.bio,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        job_postings=[]
    )


@router.get("/me", response_model=schemas.RecruiterProfileRead)
async def read_recruiter_profile_for_current_user(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_recruiter)
) -> Any:
    """
    Get the recruiter profile for the current authenticated recruiter user.
    """
    profile = current_user.recruiter_profile

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found for this user."
        )

    return schemas.RecruiterProfileRead(
        id=profile.id,
        user_id=profile.user_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        company_name=profile.company_name,
        job_title=profile.job_title,
        location=profile.location,
        phone_number=profile.phone_number,
        website_url=profile.website_url,
        linkedin_profile_url=profile.linkedin_profile_url,
        bio=profile.bio,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        job_postings=[schemas.JobPostingRead.model_validate(jp) for jp in profile.job_postings] if profile.job_postings else []
    )


@router.put("/me", response_model=schemas.RecruiterProfileRead)
async def update_recruiter_profile_for_current_user(
    profile_in: schemas.RecruiterProfileUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_recruiter)
) -> Any:
    """
    Update the recruiter profile for the current authenticated recruiter user.
    """
    profile = current_user.recruiter_profile

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found for this user."
        )

    updated_profile = await crud.recruiter_profile.update(db=db, db_obj=profile, obj_in=profile_in)

    await db.refresh(current_user, attribute_names=['recruiter_profile'])

    return schemas.RecruiterProfileRead(
        id=updated_profile.id,
        user_id=updated_profile.user_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        company_name=updated_profile.company_name,
        job_title=updated_profile.job_title,
        location=updated_profile.location,
        phone_number=updated_profile.phone_number,
        website_url=updated_profile.website_url,
        linkedin_profile_url=updated_profile.linkedin_profile_url,
        bio=updated_profile.bio,
        created_at=updated_profile.created_at,
        updated_at=updated_profile.updated_at,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        job_postings=[schemas.JobPostingRead.model_validate(jp) for jp in updated_profile.job_postings] if updated_profile.job_postings else []
    )


@router.delete("/me", response_model=schemas.RecruiterProfileRead)
async def delete_recruiter_profile_for_current_user(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_recruiter)
) -> Any:
    """
    Delete the recruiter profile for the current authenticated recruiter user.
    """
    profile = current_user.recruiter_profile

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found for this user."
        )

    deleted_profile = await crud.recruiter_profile.remove(db=db, id=profile.id)

    if not deleted_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete recruiter profile."
        )

    return schemas.RecruiterProfileRead(
        id=deleted_profile.id,
        user_id=deleted_profile.user_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        company_name=deleted_profile.company_name,
        job_title=deleted_profile.job_title,
        location=deleted_profile.location,
        phone_number=deleted_profile.phone_number,
        website_url=deleted_profile.website_url,
        linkedin_profile_url=deleted_profile.linkedin_profile_url,
        bio=deleted_profile.bio,
        created_at=deleted_profile.created_at,
        updated_at=deleted_profile.updated_at,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        job_postings=[]
    )

