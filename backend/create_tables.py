# Import models to register their table definitions with Base.metadata.
import backend.models
from backend.database import Base, engine

# Create all tables defined in the registered models.
# SQLAlchemy checks which tables already exist and only creates missing ones.
Base.metadata.create_all(bind=engine)

print("Tables created successfully.")
