from typing import Generator, Optional, Any, AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.schemas.token import TokenData
from app.crud import crud_user
from app.models.user import User, UserRole
from app.crud.crud_recruiter_profile import recruiter_profile as crud_recruiter_profile_instance
from app.models.recruiter_profile import RecruiterProfile
from app.core.config import settings
from app.database.database import get_db


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronous Database session dependency.
    Provides a SQLAlchemy AsyncSession for request handling and closes it afterwards.
    """
    from app.database.database import AsyncSessionLocal 
    async with AsyncSessionLocal() as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    Dependency to get the current user from a JWT token and database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception


    except (JWTError, AttributeError):
        raise credentials_exception

    user = await crud_user.get_user_by_id(db, id=int(user_id))

    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get the current active user.
    Requires the user to be found in the database and be active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get the current superuser.
    Requires the user to be found in the database and be a superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

async def get_current_active_recruiter( 
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> RecruiterProfile:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_from_token = payload.get("sub")
        if user_id_from_token is None:
            raise credentials_exception
        user_id = int(user_id_from_token)
    except (JWTError, ValueError, TypeError): 
        raise credentials_exception
    recruiter_profile = await crud_recruiter_profile_instance.get_by_user_id(db, user_id=user_id)
    
    if recruiter_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile for this user not found."
        )

    return recruiter_profile

async def get_current_active_candidate(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Dependency to get the current active candidate user.
    Requires the user to be active and have the 'candidate' role.
    """
    if current_user.role != UserRole.candidate:
         raise HTTPException(
            status_code=403, detail="User does not have candidate privileges"
        )
    return current_user

