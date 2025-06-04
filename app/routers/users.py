from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas 
from app.models.user import User 
from app.dependencies import deps 
from app.core.security import get_current_active_user

router = APIRouter(
    prefix="/users", 
    tags=["users"], 
    responses={404: {"description": "Not found"}},
)

@router.get("/me", response_model=schemas.User)
def read_current_user(

    current_user: User = Depends(deps.get_current_user) 

) -> Any:
    """
    Get the current authenticated user's details.
    Requires a valid JWT token in the Authorization: Bearer header.
    """
    return current_user 

@router.get("/me/candidate-data", response_model=schemas.User)
async def read_current_candidate_data(
    current_candidate: schemas.User = Depends(deps.get_current_active_candidate),
) -> Any:
    """
    Get data specific to the current candidate user.
    """
    return current_candidate

@router.get("/me/recruiter-data", response_model=schemas.User)
async def read_current_recruiter_data(

    current_recruiter: schemas.User = Depends(deps.get_current_active_recruiter),
) -> Any:
    """
    Get data specific to the current recruiter user.
    """
    return current_recruiter


@router.get("/admin-only", response_model=schemas.User)
async def read_admin_only_data(
    current_superuser: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Access point for superusers only.
    """
    return current_superuser
