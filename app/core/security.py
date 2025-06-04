from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from app.schemas.token import TokenData 
from app import crud, schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession 
from jose import JWTError, jwt
from app.dependencies import deps  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = settings.ALGORITHM

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    role: Optional[str] = None
) -> str:
    """
    Creates a new JWT access token.
    :param subject: The subject of the token (e.g., user ID or email).
    :param expires_delta: Optional timedelta for token expiration. If None, uses default.
    :param roles: Optional list of roles to include in the token payload.
    :return: The encoded JWT token string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    if role is not None:
        to_encode["role"] = role


    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a new JWT refresh token.
    :param subject: The subject of the token (e.g., user ID or email).
    :param expires_delta: Optional timedelta for token expiration. If None, uses default.
    :return: The encoded JWT token string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES 
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    :param plain_password: The plain text password.
    :param hashed_password: The hashed password from storage.
    :return: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password.
    :param password: The plain text password.
    :return: The hashed password string.
    """
    return pwd_context.hash(password)

async def get_current_user(
    db: AsyncSession = Depends(deps.get_db), 
    token: str = Depends(oauth2_scheme)
) -> schemas.User:
    """
    Decodes the JWT token and fetches the user from the database.
    Raises HTTPException if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(email=email)
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    """
    Ensures the current user is active (not disabled).
    """
    if not current_user.is_active: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def get_current_active_user_with_role(required_role: str):
    async def get_current_user_with_role(
        current_user: schemas.User = Depends(get_current_active_user),
    ) -> schemas.User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to perform this action. Requires '{required_role}' role.",
            )
        return current_user
    return get_current_user_with_role