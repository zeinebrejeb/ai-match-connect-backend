from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.dependencies import deps
from fastapi import Header
from app.schemas.token import RefreshTokenRequest 

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=schemas.User)
async def register_user(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    """
    Registers a new user.
    """
    user = await crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists.",
        )
    user = await crud.create_user(db=db, user_in=user_in) 
    return user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    """
    OAuth2 compatible token endpoint, gets an access token for a user.
    """
    user = await crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_role = user.role.value if user.role  else "user"
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
        role=user_role
    )

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = security.create_refresh_token(
        subject=user.email,
        expires_delta=refresh_token_expires
    )
    return {"access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token}

@router.post("/token/refresh", response_model=schemas.Token)
async def refresh_access_token(
    token_request: RefreshTokenRequest, 
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    """
    Refresh access token using a refresh token from the request body.
    """
    token = token_request.refresh_token

    try:
        payload = security.decode_token(token, verify_exp=True)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload.")

    user = await crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = security.create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
        role=user.role.value if user.role else "user"
    )

    return {"access_token": new_access_token, "token_type": "bearer"}
@router.get("/test-auth", response_model=schemas.User)
async def test_auth(
    current_user: schemas.User = Depends(deps.get_current_active_user) 
):
    return current_user