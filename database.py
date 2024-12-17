from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from main import DATABASE_URL

Base = declarative_base()

# Create the engine using the DATABASE_URL imported from main.py
engine = create_engine(DATABASE_URL, echo=True)

# Create a SessionLocal class to use sessions in endpoints
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a DB session in endpoint functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
