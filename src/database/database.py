import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

load_dotenv()  # Loads .env values into environment

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "prices_db")

DATABASE_URL = (
    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()