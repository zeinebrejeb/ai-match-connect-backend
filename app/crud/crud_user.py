from typing import Any, Dict, Optional, Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.models.candidate_profile import CandidateProfile
from app.models.recruiter_profile import RecruiterProfile 
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Retrieves a user from the database by their ID (asynchronous).
    Eagerly loads candidate_profile/recruiter_profile and their nested relationships.
    """
    statement = (
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.candidate_profile).options(
                selectinload(CandidateProfile.experiences),
                selectinload(CandidateProfile.educations),
                selectinload(CandidateProfile.candidate_skills)
            ),
            selectinload(User.recruiter_profile).options(
                selectinload(RecruiterProfile.job_postings) 
            )
        )
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Retrieves a user from the database by their email address (asynchronous).
    Eagerly loads candidate_profile/recruiter_profile and their nested relationships.
    """
    statement = (
        select(User)
        .where(User.email == email)
        .options(
            selectinload(User.candidate_profile).options(
                selectinload(CandidateProfile.experiences),
                selectinload(CandidateProfile.educations),
                selectinload(CandidateProfile.candidate_skills)
            ),
            selectinload(User.recruiter_profile).options(
                selectinload(RecruiterProfile.job_postings)
            )
        )
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieves a list of users with optional pagination (asynchronous).
    Eagerly loads candidate_profile/recruiter_profile and their nested relationships for each user.
    """
    statement = (
        select(User)
        .offset(skip)
        .limit(limit)
        .options(
            selectinload(User.candidate_profile).options(
                selectinload(CandidateProfile.experiences),
                selectinload(CandidateProfile.educations),
                selectinload(CandidateProfile.candidate_skills)
            ),
            selectinload(User.recruiter_profile).options(
                selectinload(RecruiterProfile.job_postings)
            )
        )
        .order_by(User.id)
    )
    result = await db.execute(statement)
    return result.scalars().unique().all()

async def create_user(db: AsyncSession, *, user_in: UserCreate) -> User:
    """
    Creates a new user in the database (asynchronous).
    Hashes the password before saving.
    """
    hashed_password = get_password_hash(user_in.password)
    create_data = user_in.model_dump(exclude={"password"})
    
    db_user = User(**create_data, hashed_password=hashed_password)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    loaded_user = await get_user(db, user_id=db_user.id)
    if not loaded_user:
        raise Exception("Failed to retrieve newly created user with relationships.")
    return loaded_user

async def update_user(
    db: AsyncSession, *, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    """
    Updates an existing user in the database (asynchronous).
    Handles hashing the password if it's included in the update data.
    """
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    else:
        update_data.pop("password", None)

    for field, value in update_data.items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    loaded_user = await get_user(db, user_id=db_user.id)
    if not loaded_user:
        raise Exception("Failed to retrieve updated user with relationships.")
    return loaded_user

async def delete_user(db: AsyncSession, *, user_id: int) -> Optional[User]:
    """
    Deletes a user from the database by their ID (asynchronous).
    Returns the deleted user object, or None if not found.
    """
    db_user = await get_user(db, user_id=user_id)

    if db_user:
        await db.delete(db_user)
        await db.commit()
        return db_user
    return None

