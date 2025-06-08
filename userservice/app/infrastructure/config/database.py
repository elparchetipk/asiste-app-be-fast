"""Database configuration for user service."""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from app.config import settings
from ..models import Base


class DatabaseConfig:
    """Database configuration class."""
    
    def __init__(self):
        self.database_url = settings.DATABASE_URL
        self.engine = create_async_engine(
            self.database_url,
            echo=settings.DATABASE_ECHO,
            poolclass=NullPool if os.getenv("ENVIRONMENT") == "test" else None,
        )
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    
    async def create_tables(self) -> None:
        """Create database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self) -> None:
        """Drop database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def close(self) -> None:
        """Close database engine."""
        await self.engine.dispose()


# Global database configuration instance
database_config = DatabaseConfig()
engine = database_config.engine


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection."""
    async with database_config.async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_health() -> bool:
    """Check database connection health."""
    try:
        async with database_config.async_session_maker() as session:
            await session.execute(text("SELECT 1"))
            return True
    except Exception:
        return False
