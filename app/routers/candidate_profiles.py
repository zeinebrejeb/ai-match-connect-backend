from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.models.user import User
from app.dependencies import deps

router = APIRouter(
    prefix="/candidate-profiles",
    tags=["candidate-profiles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.CandidateProfileRead, status_code=status.HTTP_201_CREATED)
async def create_candidate_profile_for_current_user(
    profile_in: schemas.CandidateProfileCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_candidate)
) -> Any:
    """
    Create a candidate profile for the current authenticated candidate user.
    A candidate user can only have one profile.
    """
    if current_user.candidate_profile:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a candidate profile."
        )

    profile = await crud.candidate_profile.create_with_owner(
        db=db,
        user_id=current_user.id,
        obj_in=profile_in
    )

    return schemas.CandidateProfileRead(
        id=profile.id,
        user_id=profile.user_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        bio=profile.bio,
        phone_number=profile.phone_number,
        location=profile.location,
        linkedin_profile_url=profile.linkedin_profile_url,
        portfolio_url=profile.portfolio_url,
        resume_url=profile.resume_url,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        experiences=[schemas.ExperienceData.model_validate(exp) for exp in profile.experiences] if profile.experiences else [],
        educations=[schemas.EducationData.model_validate(edu) for edu in profile.educations] if profile.educations else [],
        skills=[schemas.CandidateSkillBase.model_validate(skill) for skill in profile.candidate_skills] if profile.candidate_skills else []
    )


@router.get("/me", response_model=schemas.CandidateProfileRead)
async def read_candidate_profile_for_current_user(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_candidate)
) -> Any:
    """
    Get the candidate profile for the current authenticated candidate user.
    """
    profile = current_user.candidate_profile

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found for this user."
        )

    return schemas.CandidateProfileRead(
        id=profile.id,
        user_id=profile.user_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        bio=profile.bio,
        phone_number=profile.phone_number,
        location=profile.location,
        linkedin_profile_url=profile.linkedin_profile_url,
        portfolio_url=profile.portfolio_url,
        resume_url=profile.resume_url,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        experiences=[schemas.ExperienceData.model_validate(exp) for exp in profile.experiences] if profile.experiences else [],
        educations=[schemas.EducationData.model_validate(edu) for edu in profile.educations] if profile.educations else [],
        skills=[schemas.CandidateSkillBase.model_validate(skill) for skill in profile.candidate_skills] if profile.candidate_skills else []
    )


@router.put("/me", response_model=schemas.CandidateProfileRead)
async def update_candidate_profile_for_current_user(
    profile_in: schemas.CandidateProfileUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_candidate)
) -> Any:
    """
    Update the candidate profile for the current authenticated candidate user.
    """
    profile = current_user.candidate_profile

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found for this user."
        )

    updated_profile = await crud.candidate_profile.update(db=db, db_obj=profile, obj_in=profile_in)

    await db.refresh(current_user, attribute_names=['candidate_profile'])

    return schemas.CandidateProfileRead(
        id=updated_profile.id,
        user_id=updated_profile.user_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        bio=updated_profile.bio,
        phone_number=updated_profile.phone_number,
        location=updated_profile.location,
        linkedin_profile_url=updated_profile.linkedin_profile_url,
        portfolio_url=updated_profile.portfolio_url,
        resume_url=updated_profile.resume_url,
        created_at=updated_profile.created_at,
        updated_at=updated_profile.updated_at,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        experiences=[schemas.ExperienceData.model_validate(exp) for exp in updated_profile.experiences] if updated_profile.experiences else [],
        educations=[schemas.EducationData.model_validate(edu) for edu in updated_profile.educations] if updated_profile.educations else [],
        skills=[schemas.CandidateSkillBase.model_validate(skill) for skill in updated_profile.candidate_skills] if updated_profile.candidate_skills else []
    )


@router.delete("/me", response_model=schemas.CandidateProfileRead)
async def delete_candidate_profile_for_current_user(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_candidate)
) -> Any:
    """
    Delete the candidate profile for the current authenticated candidate user.
    """
    profile = current_user.candidate_profile

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found for this user."
        )

    deleted_profile = await crud.candidate_profile.remove(db=db, id=profile.id)

    if not deleted_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete candidate profile."
        )

    return schemas.CandidateProfileRead(
        id=deleted_profile.id,
        user_id=deleted_profile.user_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        bio=deleted_profile.bio,
        phone_number=deleted_profile.phone_number,
        location=deleted_profile.location,
        linkedin_profile_url=deleted_profile.linkedin_profile_url,
        portfolio_url=deleted_profile.portfolio_url,
        resume_url=deleted_profile.resume_url,
        created_at=deleted_profile.created_at,
        updated_at=deleted_profile.updated_at,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
        experiences=[],
        educations=[],
        skills=[]
    )

