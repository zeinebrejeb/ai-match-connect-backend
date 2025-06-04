from typing import Any, Dict, Optional, Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.base import CRUDBase 
from app.models.job_posting import JobPosting 
from app.schemas.job_posting import JobPostingCreate, JobPostingUpdate 

def skills_list_to_string(skills: List[str]) -> str:
    """Converts a list of skill strings into a single string for storage."""
    return ", ".join(skill.strip() for skill in skills if skill.strip()) 

# Helper function to convert a string of skills back to a list
def skills_string_to_list(skills_string: Optional[str]) -> List[str]:
    """Converts a string of skills (e.g., comma-separated) back into a list."""
    if not skills_string:
        return []
    # Split by comma and space, strip whitespace from each item
    return [skill.strip() for skill in skills_string.split(',') if skill.strip()]


# Create a specific CRUD class for JobPosting, inheriting from CRUDBase
class CRUDJobPosting(CRUDBase[JobPosting, JobPostingCreate, JobPostingUpdate]):

    async def get_by_recruiter_profile_id(
        self, db: AsyncSession, *, recruiter_profile_id: int, skip: int = 0, limit: int = 100
    ) -> List[JobPosting]:
        """
        Retrieves job postings associated with a specific recruiter profile.
        """
        statement = (
            select(self.model) 
            .where(self.model.recruiter_profile_id == recruiter_profile_id)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.created_at.desc()) 
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def create_with_recruiter_profile(
        self, db: AsyncSession, *, obj_in: JobPostingCreate, recruiter_profile_id: int
    ) -> JobPosting:
        """
        Creates a new job posting linked to a recruiter profile.
        Handles conversion of skills list to string.
        """
        # Convert Pydantic schema to dictionary, excluding unset fields
        create_data = obj_in.model_dump(exclude_unset=True) 

        # Convert the list of skills to the string format for the model
        skills_string = skills_list_to_string(create_data.pop("skills", []))

        # Create the SQLAlchemy model instance, adding the foreign key and skills string
        db_obj = self.model(
            **create_data,
            recruiter_profile_id=recruiter_profile_id,
            required_skills=skills_string # Map schema 'skills' to model 'required_skills'
        ) # Use self.model

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update( # Override the base update to handle skills conversion
        self,
        db: AsyncSession,
        *,
        db_obj: JobPosting,
        obj_in: Union[JobPostingUpdate, Dict[str, Any]] 
    ) -> JobPosting:
        """
        Updates an existing job posting.
        Handles conversion of skills list to string if skills are updated.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Convert Pydantic schema to dictionary, excluding unset fields
            update_data = obj_in.model_dump(exclude_unset=True) # Use model_dump for Pydantic v2+

        # Handle the 'skills' field specifically if it's in the update data
        if "skills" in update_data:
            skills_list = update_data.pop("skills") # Get the list of skills
            if skills_list is not None: # Check if skills were explicitly provided (could be None for Optional)
                update_data["required_skills"] = skills_list_to_string(skills_list) # Convert and add to update data
            else:
                 # If skills was explicitly set to None in the schema, set required_skills to None/empty string
                 update_data["required_skills"] = None # Or "" depending on how you want to represent empty skills


        # Apply updates to the db_obj using the modified update_data
        for field, value in update_data.items():
             if hasattr(db_obj, field): # Check if the model has the attribute
                setattr(db_obj, field, value)

        db.add(db_obj) 
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

job_posting = CRUDJobPosting(JobPosting)

#now use job_posting.get, job_posting.get_multi, job_posting.get_by_recruiter_profile_id,
# job_posting.create_with_recruiter_profile, job_posting.update, job_posting.remove
