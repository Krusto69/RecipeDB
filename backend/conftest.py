# This is a special file name recognised by pytest to define shared testing fixtured to be reused across multiple test files

import os

import models  # Register all models with Base.metadata
import pytest
from database import Base
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

@pytest.fixture(scope="session")
def test_engine():
    # Safety check: prevent accidentally dropping tables in our main database.
    if os.getenv("TEST_DB_NAME") != "recipeDB_test":
        raise RuntimeError("Incorrect test database configured!")

    # Build the connection URL using our test database settings.
    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("TEST_DB_USER"),
        password=os.getenv("TEST_DB_PASSWORD"),
        host=os.getenv("TEST_DB_HOST"),
        port=int(os.getenv("TEST_DB_PORT", "5432")),
        database=os.getenv("TEST_DB_NAME"),
    )

    engine = create_engine(database_url)

    # Create all tables before running the tests.
    Base.metadata.create_all(bind=engine)

    yield engine

    # Remove the tables after the entire test run finishes.
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    # Each test gets its own connection and transaction.
    connection = test_engine.connect()
    transaction = connection.begin()

    TestSession = sessionmaker(bind=connection)
    session = TestSession()

    yield session

    # Close the session and roll back any changes made by the test.
    session.close()
    # If a transaction fails then it will be closed automatically, so we check if it still exist first
    if transaction.is_active:
        transaction.rollback()
    connection.close()
