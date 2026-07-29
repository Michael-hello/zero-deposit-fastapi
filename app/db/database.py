import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from alembic import op

load_dotenv()  


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev2.db")
MODE = os.getenv("MODE", "dev")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=True  # Set to False in production
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    #Initialize database by automatically creating all tables if necessary
    Base.metadata.create_all(bind=engine)
    if MODE == "dev":
        seed_db()


def seed_db():
    # Seed the database with initial data for development
    from app.api.property.model import Property
    from sqlalchemy.orm import Session

    db: Session = SessionLocal()

    # Check if properties already exist to avoid duplicate seeding
    if db.query(Property).count() == 0:
        sample_properties = [
            Property(address="123 Main St", postcode="12345", city="Anytown", rooms=3, created_by="seed"),
            Property(address="456 Elm St", postcode="67890", city="Othertown", rooms=2, created_by="seed"),
        ]
        db.add_all(sample_properties)
        db.commit()
    db.close()
