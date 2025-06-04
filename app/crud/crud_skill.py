from typing import Any, Dict, Optional, Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.base import CRUDBase 
from app.models.skill import CandidateSkill 
from app.schemas.skill import CandidateSkillCreate, CandidateSkillUpdate 

class CRUDCandidateSkill(CRUDBase[CandidateSkill, CandidateSkillCreate, CandidateSkillUpdate]):

    async def get_by_candidate_profile_id(
        self, db: AsyncSession, *, candidate_profile_id: int, skip: int = 0, limit: int = 100
    ) -> List[CandidateSkill]:
        """
        Récupère les entrées de compétence associées à un profil candidat.
        """
        statement = (
            select(self.model) 
            .where(self.model.candidate_profile_id == candidate_profile_id)
            .offset(skip)
            .limit(limit)
            .order_by(CandidateSkill.name) 
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def create_with_profile(
        self, db: AsyncSession, *, obj_in: CandidateSkillCreate, candidate_profile_id: int
    ) -> CandidateSkill:
        """
        Crée une nouvelle entrée de compétence liée à un profil candidat.
        """
        
        obj_in_data = obj_in.model_dump(exclude_unset=True) 

        db_obj = self.model(**obj_in_data, candidate_profile_id=candidate_profile_id)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

candidate_skill = CRUDCandidateSkill(CandidateSkill)

#now use candidate_skill.get, candidate_skill.get_multi, candidate_skill.get_by_candidate_profile_id,
# candidate_skill.create_with_profile, candidate_skill.update, candidate_skill.remove
