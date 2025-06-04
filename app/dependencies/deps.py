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
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except (JWTError, AttributeError):
        raise credentials_exception

    user = await crud_user.get_user_by_email(db, email=token_data.email)

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
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Dependency to get the current active recruiter user.
    Requires the user to be active and have the 'recruiter' role.
    """
    if current_user.role != UserRole.recruiter:
         raise HTTPException(
            status_code=403, detail="User does not have recruiter privileges"
        )
    return current_user

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

