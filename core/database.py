from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import DATABASE_PATH
from models.base import Base

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Returns a database session.
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def initialize_database():
    """
    Creates all database tables.
    """

    Base.metadata.create_all(bind=engine)

    print("✅ Database initialized successfully!")