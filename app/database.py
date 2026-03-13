from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# The Engine creates the connection pool 🏊
engine = create_engine(
    settings.DATABASE_URL,
    # Standard for MySQL/PyMySQL to prevent "Connection closed" errors
    pool_pre_ping=True 
)

# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy Models
Base = declarative_base()

# The "Dependency" we will use in our routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()