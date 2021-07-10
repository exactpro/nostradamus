import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


DB_NAME = os.environ.get("POSTGRES_DB", "users")
DB_USER = os.environ.get("POSTGRES_USER", "postgres_user")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres_password")
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def create_session() -> Session:
    """Create database session.

    :return: Database session.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
