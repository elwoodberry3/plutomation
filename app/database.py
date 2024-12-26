# 'DATABASE' - Handles database session management and engine creation.
# Last updated on 12.26.2024

import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Environment variable: DATABASE_URL
# Specifies the connection string for the database. Defaults to a PostgreSQL database hosted locally.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/plutomation_db")

# Environment variable: DB_ECHO
# If set to "true" (case insensitive), enables SQLAlchemy's logging of all executed SQL statements.
# Defaults to "false".
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DB_ECHO", "false").lower() == "true",
    
    # Environment variable: DB_POOL_SIZE
    # Determines the size of the database connection pool. Defaults to 5.
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    
    # Environment variable: DB_MAX_OVERFLOW
    # Sets the number of connections that can be created beyond the pool_size. Defaults to 10.
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
)

# Creates an async session maker for database interactions
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """
    Database session generator for dependency injection.
    Provides an async database session and ensures it is properly closed after use.
    """
    async with async_session() as session:
        yield session

