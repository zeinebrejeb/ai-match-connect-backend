from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from typing import AsyncGenerator # Import AsyncGenerator

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# Dependency to get a database session
async def get_db() -> AsyncGenerator[AsyncSession, None]: # Use AsyncGenerator for proper typing
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Commits and rollbacks should ideally be handled in the endpoint/service layer
            # where the specific database operations are performed.
            # If an unhandled exception occurs before commit in the endpoint,
            # the 'async with' block will ensure the transaction is not committed.
        except Exception:
            # If an exception occurs during the session usage in the endpoint,
            # it will propagate here. You might want to log it.
            # The transaction will be rolled back automatically by SQLAlchemy
            # when the session context manager exits due to an exception,
            # unless session.commit() was already called successfully.
            # Explicit rollback here can be redundant if commit isn't called in this dependency.
            # However, if you want to be absolutely sure:
            # await session.rollback() # This might be redundant if commit is not attempted here
            raise # Re-raise the exception so FastAPI can handle it
        finally:
            await session.close()