

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base


def init_test_db():
    """ Initializes the test database and returns a session """

    SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Creates all tables
    Base.metadata.create_all(bind=engine)
    
    return TestingSessionLocal()