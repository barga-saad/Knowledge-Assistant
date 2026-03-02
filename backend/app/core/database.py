"""
Database connection and session management
Uses SQLAlchemy with async support
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create async database engine
# psycopg is the PostgreSQL driver for SQLAlchemy 2.0+
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql+psycopg://", "postgresql+asyncpg://"),
    echo=settings.BACKEND_ENV == "development",  # Log SQL in dev
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Base class for all SQLAlchemy models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency injection for database sessions.
    
    Usage in FastAPI endpoints:
        async def my_endpoint(db: AsyncSession = Depends(get_db)):
            # Use db session
    
    This ensures the session is properly closed after each request.
    """
    async with AsyncSessionLocal() as session:
        yield session
