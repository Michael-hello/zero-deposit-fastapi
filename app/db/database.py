import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator

load_dotenv()  


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev2.db")

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
