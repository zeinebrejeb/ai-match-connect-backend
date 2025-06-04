from typing import Any, Dict, Optional, Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.base import CRUDBase 
from app.models.experience import Experience 
from app.schemas.experience import ExperienceCreate, ExperienceUpdate 

class CRUDExperience(CRUDBase[Experience, ExperienceCreate, ExperienceUpdate]):

    async def get_by_candidate_profile_id(
        self, db: AsyncSession, *, candidate_profile_id: int, skip: int = 0, limit: int = 100
    ) -> List[Experience]:
        """
        Récupère les entrées d'expérience associées à un profil candidat.
        """
        statement = (
            select(self.model)
            .where(self.model.candidate_profile_id == candidate_profile_id)
            .offset(skip)
            .limit(limit)
            .order_by(Experience.start_date.desc()) 
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def create_with_profile(
        self, db: AsyncSession, *, obj_in: ExperienceCreate, candidate_profile_id: int
    ) -> Experience:
        """
        Crée une nouvelle entrée d'expérience liée à un profil candidat.
        """
        obj_in_data = obj_in.model_dump(exclude_unset=True) 

        db_obj = self.model(**obj_in_data, candidate_profile_id=candidate_profile_id) 

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

experience = CRUDExperience(Experience)

#use experience.get, experience.get_multi, experience.get_by_candidate_profile_id,
# experience.create_with_profile, experience.update, experience.remove
