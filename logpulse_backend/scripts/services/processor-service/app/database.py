import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Environment variable එකෙන් DB URL එක ලබා ගැනීම
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://auth_user:password@postgres:5432/auth_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# FastAPI routes සඳහා DB Session dependency එක
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
