from typing import Any, Dict, Optional, Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.crud.base import CRUDBase 
from app.models.recruiter_profile import RecruiterProfile 
from app.models.job_posting import JobPosting 
from app.schemas.recruiter_profile import RecruiterProfileCreate, RecruiterProfileUpdate 

class CRUDRecruiterProfile(CRUDBase[RecruiterProfile, RecruiterProfileCreate, RecruiterProfileUpdate]):

    async def get_by_user_id(
        self, db: AsyncSession, *, user_id: int
    ) -> Optional[RecruiterProfile]:
        """
        Retrieves a recruiter profile by user ID, eagerly loading related data.
        """
        statement = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(
                selectinload(self.model.job_postings) 
        
            )
        )
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: RecruiterProfileCreate, user_id: int
    ) -> RecruiterProfile:
        """
        Creates a new recruiter profile linked to a user.
        """
        create_data = obj_in.model_dump(exclude_unset=True)

        db_obj = self.model(**create_data, user_id=user_id)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        loaded_db_obj = await self.get_by_user_id(db, user_id=user_id)
        if not loaded_db_obj:
            raise Exception("Failed to retrieve newly created profile with relationships.")
        return loaded_db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: RecruiterProfile,
        obj_in: Union[RecruiterProfileUpdate, Dict[str, Any]]
    ) -> RecruiterProfile:
        """
        Updates an existing recruiter profile.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        loaded_db_obj = await self.get_by_user_id(db, user_id=db_obj.user_id)
        if not loaded_db_obj:
            raise Exception("Failed to retrieve updated profile with relationships.")
        return loaded_db_obj

recruiter_profile = CRUDRecruiterProfile(RecruiterProfile) 
