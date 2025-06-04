from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.models.user import User, UserRole
from app.dependencies import deps 

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

get_current_admin_user = deps.get_current_active_superuser

@router.get("/users", response_model=List[schemas.User])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user)
) -> Any:
    """
    Retrieve all users (admin only).
    """
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> Any:
    """
    Retrieve a specific user by ID (admin only).
    """
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user_by_admin(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> Any:
    """
    Update a user's details by ID (admin only).
    Admin can change roles, active status, etc.
    """
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    # Prevent admin from deactivating themselves or changing their own superuser status
    if user.id == current_admin.id and (user_in.is_active is False or user_in.is_superuser is False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin cannot deactivate or remove superuser status from themselves."
        )
    
    #Prevent changing an admin's role if not explicitly allowed
    if user.role == UserRole.admin and user_in.role and user_in.role != UserRole.admin:
         raise HTTPException(
             status_code=status.HTTP_403_FORBIDDEN,
             detail="Admin cannot change another admin's role."
         )

    updated_user = await crud.update_user(db=db, db_user=user, user_in=user_in)
    return updated_user

@router.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user_by_admin(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> Any:
    """
    Delete a user by ID (admin only).
    """
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin cannot delete their own account."
        )
    user = await crud.delete_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/recruiter-profiles", response_model=List[schemas.RecruiterProfileRead])
async def read_all_recruiter_profiles(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user)
) -> Any:
    """
    Retrieve all recruiter profiles (admin only).
    """
    recruiter_profiles = await crud.recruiter_profile.get_multi(db, skip=skip, limit=limit)
    
    results = []
    for profile in recruiter_profiles:
        # Ensure the user relationship is loaded 
        if profile.user:
            results.append(schemas.RecruiterProfileRead(
                id=profile.id,
                user_id=profile.user_id,
                first_name=profile.user.first_name,
                last_name=profile.user.last_name,
                email=profile.user.email,
                is_active=profile.user.is_active,
                role=profile.user.role,
                company_name=profile.company_name,
                job_title=profile.job_title,
                location=profile.location,
                phone_number=profile.phone_number,
                website_url=profile.website_url,
                linkedin_profile_url=profile.linkedin_profile_url,
                bio=profile.bio,
                created_at=profile.created_at,
                updated_at=profile.updated_at,
                job_postings=[schemas.JobPostingRead.model_validate(jp) for jp in profile.job_postings] if profile.job_postings else []
            ))
        else:
            # Handle case where user relationship is not loaded or missing
            results.append(schemas.RecruiterProfileRead(
                id=profile.id,
                user_id=profile.user_id,
                email="N/A", 
                is_active=False,
                role="N/A",
                company_name=profile.company_name,
                job_title=profile.job_title,
                location=profile.location,
                phone_number=profile.phone_number,
                website_url=profile.website_url,
                linkedin_profile_url=profile.linkedin_profile_url,
                bio=profile.bio,
                created_at=profile.created_at,
                updated_at=profile.updated_at,
                job_postings=[]
            ))
    return results

@router.get("/recruiter-profiles/{profile_id}", response_model=schemas.RecruiterProfileRead)
async def read_recruiter_profile_by_id(
    profile_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> Any:
    """
    Retrieve a specific recruiter profile by ID (admin only).
    """
    profile = await crud.recruiter_profile.get(db, id=profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found"
        )
    
    # Ensure user relationship is loaded for the response model
    if profile.user:
        return schemas.RecruiterProfileRead(
            id=profile.id,
            user_id=profile.user_id,
            first_name=profile.user.first_name,
            last_name=profile.user.last_name,
            email=profile.user.email,
            is_active=profile.user.is_active,
            role=profile.user.role,
            company_name=profile.company_name,
            job_title=profile.job_title,
            location=profile.location,
            phone_number=profile.phone_number,
            website_url=profile.website_url,
            linkedin_profile_url=profile.linkedin_profile_url,
            bio=profile.bio,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            job_postings=[schemas.JobPostingRead.model_validate(jp) for jp in profile.job_postings] if profile.job_postings else []
        )
    else:
        # Fallback if user relationship is not loaded
        return schemas.RecruiterProfileRead(
            id=profile.id,
            user_id=profile.user_id,
            email="N/A",
            is_active=False,
            role="N/A",
            company_name=profile.company_name,
            job_title=profile.job_title,
            location=profile.location,
            phone_number=profile.phone_number,
            website_url=profile.website_url,
            linkedin_profile_url=profile.linkedin_profile_url,
            bio=profile.bio,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            job_postings=[]
        )


@router.put("/recruiter-profiles/{profile_id}", response_model=schemas.RecruiterProfileRead)
async def update_recruiter_profile_by_admin(
    profile_id: int,
    profile_in: schemas.RecruiterProfileUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> Any:
    """
    Update a recruiter profile by ID (admin only).
    """
    profile = await crud.recruiter_profile.get(db, id=profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found"
        )
    
    updated_profile = await crud.recruiter_profile.update(db=db, db_obj=profile, obj_in=profile_in)

    # Re-fetch the user to ensure updated recruiter_profile relationship is loaded for response
    updated_user = await crud.get_user(db, user_id=updated_profile.user_id)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Associated user not found after profile update."
        )

    return schemas.RecruiterProfileRead(
        id=updated_profile.id,
        user_id=updated_profile.user_id,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        email=updated_user.email,
        is_active=updated_user.is_active,
        role=updated_user.role,
        company_name=updated_profile.company_name,
        job_title=updated_profile.job_title,
        location=updated_profile.location,
        phone_number=updated_profile.phone_number,
        website_url=updated_profile.website_url,
        linkedin_profile_url=updated_profile.linkedin_profile_url,
        bio=updated_profile.bio,
        created_at=updated_profile.created_at,
        updated_at=updated_profile.updated_at,
        job_postings=[schemas.JobPostingRead.model_validate(jp) for jp in updated_profile.job_postings] if updated_profile.job_postings else []
    )

@router.delete("/recruiter-profiles/{profile_id}", response_model=schemas.RecruiterProfileRead)
async def delete_recruiter_profile_by_admin(
    profile_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> Any:
    """
    Delete a recruiter profile by ID (admin only).
    This will also delete the associated User if cascade is set up.
    """
    profile = await crud.recruiter_profile.get(db, id=profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found"
        )
    
    deleted_profile = await crud.recruiter_profile.remove(db=db, id=profile_id)

    if not deleted_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete recruiter profile."
        )
    
    # Return the deleted profile data, potentially with user info if it was loaded
    return schemas.RecruiterProfileRead(
        id=deleted_profile.id,
        user_id=deleted_profile.user_id,
        first_name=deleted_profile.user.first_name if deleted_profile.user else None, 
        last_name=deleted_profile.user.last_name if deleted_profile.user else None,
        email=deleted_profile.user.email if deleted_profile.user else "N/A",
        is_active=deleted_profile.user.is_active if deleted_profile.user else False,
        role=deleted_profile.user.role if deleted_profile.user else "N/A",
        company_name=deleted_profile.company_name,
        job_title=deleted_profile.job_title,
        location=deleted_profile.location,
        phone_number=deleted_profile.phone_number,
        website_url=deleted_profile.website_url,
        linkedin_profile_url=deleted_profile.linkedin_profile_url,
        bio=deleted_profile.bio,
        created_at=deleted_profile.created_at,
        updated_at=deleted_profile.updated_at,
        job_postings=[] # empty after deletion
    )

