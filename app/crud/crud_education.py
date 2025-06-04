from typing import Any, Dict, Optional, Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.base import CRUDBase 
from app.models.education import Education 
from app.schemas.education import EducationCreate, EducationUpdate 

class CRUDEducation(CRUDBase[Education, EducationCreate, EducationUpdate]):

    async def get_by_candidate_profile_id(
        self, db: AsyncSession, *, candidate_profile_id: int, skip: int = 0, limit: int = 100
    ) -> List[Education]:
        """
        Récupère les entrées d'éducation associées à un profil candidat.
        """
        statement = (
            select(self.model) 
            .where(self.model.candidate_profile_id == candidate_profile_id)
            .offset(skip)
            .limit(limit)
        
            .order_by(Education.start_date.desc())
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def create_with_profile(
        self, db: AsyncSession, *, obj_in: EducationCreate, candidate_profile_id: int
    ) -> Education:
        """
        Crée une nouvelle entrée d'éducation liée à un profil candidat.
        """
        obj_in_data = obj_in.model_dump(exclude_unset=True) 

        db_obj = self.model(**obj_in_data, candidate_profile_id=candidate_profile_id) 

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

education = CRUDEducation(Education)

# education.get, education.get_multi, education.get_by_candidate_profile_id,
# education.create_with_profile, education.update, education.remove
