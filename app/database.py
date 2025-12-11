from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg
from psycopg.rows import dict_row
from .config import settings
import time

# SQLAlchemy URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Optional: test raw connection using psycopg3
while True:
    try:
        conn = psycopg.connect(
            host=settings.database_hostname,
            dbname=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
            autocommit=True
        )
        cursor = conn.cursor(row_factory=dict_row)
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(3)  # wait 3 seconds before retry
