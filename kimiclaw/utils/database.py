"""Database initialization and connection utilities."""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger

from kimiclaw.core.config import settings
from kimiclaw.models.database import Base


# Create engine
engine = create_engine(settings.database_url, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def drop_db():
    """Drop all database tables (use with caution!)."""
    try:
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped")
    except Exception as e:
        logger.error(f"Error dropping database: {e}")
        raise


@contextmanager
def get_db() -> Session:
    """Get database session context manager.
    
    Usage:
        with get_db() as db:
            db.query(Customer).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """Get a database session (for dependency injection).
    
    Usage in FastAPI:
        @app.get("/customers")
        def get_customers(db: Session = Depends(get_db_session)):
            return db.query(Customer).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
