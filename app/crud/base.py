from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select #for async queries
from sqlalchemy.orm import selectinload # For eager loading relationships

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with default async methods to Create, Read, Update, Delete (CRUD).
    """
    def __init__(self, model: Type[ModelType]):
        """
        A SQLAlchemy model class.
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Retrieve a single object by ID."""
        statement = select(self.model).where(self.model.id == id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Retrieve multiple objects with optional pagination."""
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new object."""
        # Convert Pydantic schema to dictionary, excluding unset fields
        obj_in_data = obj_in.model_dump(exclude_unset=True) 
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType, # Existing SQLAlchemy object
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing object."""
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
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """Remove an object by ID."""
        statement = select(self.model).where(self.model.id == id)
        result = await db.execute(statement)
        db_obj = result.scalar_one_or_none()

        if db_obj:
            await db.delete(db_obj)
            await db.commit()
            return db_obj
        return None

