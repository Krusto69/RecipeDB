import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase


# Base class for all SQLAlchemy models.
# Models inherit from Base, allowing SQLAlchemy to register their table definitions and manage their relationships through shared metadata.
class Base(DeclarativeBase):
    pass


# Load environment variables from the project root.
# __file__ refers to this file (database.py).
# This makes the .env file path independent of the working directory.
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


# Build the database connection URL using credentials and settings stored in environment variables.
# URL.create() handles the construction and escaping of connection details.
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)


# Create the SQLAlchemy engine.
# The engine manages database connections
# It does not establish a connection immediately; connections are opened when the application first needs to communicate with the database.
engine = create_engine(database_url)
