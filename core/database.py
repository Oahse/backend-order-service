from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from core.config import settings

Base = declarative_base()
CHAR_LENGTH=255

# Database engine
SQL_DATABASE_URI = str(settings.SQL_DATABASE_URI) 
ELASTIC_DATABASE_URI = str(settings.ELASTIC_DATABASE_URI) 


engine_db = create_async_engine(SQL_DATABASE_URI, echo=True, pool_pre_ping=True)

# Session factory for the first database (Async)
AsyncSessionDB = sessionmaker(
    bind=engine_db, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependency to get the async session for the first database
async def get_db():
    try:
        async with AsyncSessionDB() as session:
            print(f"Database connected")
            yield session
    except Exception as e:
        # Log the error or handle it accordingly
        print(f"Database connection failed: {e}")
        raise
