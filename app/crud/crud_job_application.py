from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.crud.base import CRUDBase
from app.models.job_application import JobApplication
from app.schemas.job_application import JobApplicationCreate, JobApplicationUpdate

class CRUDJobApplication(CRUDBase[JobApplication, JobApplicationCreate, JobApplicationUpdate]):
    """
    CRUD operations for JobApplication model.
    """
    async def create_with_candidate(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: JobApplicationCreate, 
        candidate_profile_id: int
    ) -> JobApplication:
        """
        Create a new job application and associate it with a candidate profile.
        """
        db_obj_data = obj_in.model_dump()
        db_obj = self.model(**db_obj_data, candidate_profile_id=candidate_profile_id)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_job_posting(
        self, 
        db: AsyncSession, 
        *, 
        job_posting_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[JobApplication]:
        """
        Retrieve all applications for a specific job posting.
        """
        result = await db.execute(
            select(self.model)
            .where(JobApplication.job_posting_id == job_posting_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_multi_by_candidate(
        self, 
        db: AsyncSession, 
        *, 
        candidate_profile_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[JobApplication]:
        """
        Retrieve all applications submitted by a specific candidate.
        """
        result = await db.execute(
            select(self.model)
            .where(JobApplication.candidate_profile_id == candidate_profile_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

job_application = CRUDJobApplication(JobApplication)

