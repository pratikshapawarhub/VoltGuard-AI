"""
VoltGuard AI - Database Configuration
Configures SQLite database and SQLAlchemy session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.config import SQLALCHEMY_DATABASE_URL

# SQLite requires connect_args check_same_thread=False for multi-threaded FastAPI workers
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    FastAPI dependency yielding a scoped database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
