from typing import Any, Dict, Optional, Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload 
from app.crud.base import CRUDBase
from app.models.candidate_profile import CandidateProfile 
from app.schemas.candidate_profile import CandidateProfileCreate, CandidateProfileUpdate 


class CRUDCandidateProfile(CRUDBase[CandidateProfile, CandidateProfileCreate, CandidateProfileUpdate]):

    async def get_by_user_id(
        self, db: AsyncSession, *, user_id: int
    ) -> Optional[CandidateProfile]:
        """
        Retrieves a candidate profile by user ID, eagerly loading related data.
        """
        statement = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(
                selectinload(self.model.experiences),
                selectinload(self.model.educations),
                selectinload(self.model.candidate_skills)
            )
        )
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: CandidateProfileCreate, user_id: int
    ) -> CandidateProfile:
        """
        Creates a new candidate profile linked to a user.
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
        db_obj: CandidateProfile,
        obj_in: Union[CandidateProfileUpdate, Dict[str, Any]]
    ) -> CandidateProfile:
        """
        Updates an existing candidate profile.
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

    # The base CRUDBase provides:
    # async def get(self, db: AsyncSession, id: Any) -> Optional[CandidateProfile]:
    # async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[CandidateProfile]:
    # async def remove(self, db: AsyncSession, *, id: int) -> Optional[CandidateProfile]:


candidate_profile = CRUDCandidateProfile(CandidateProfile)
