from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from main import DATABASE_URL

Base = declarative_base()

# Import your models AFTER Base is declared but BEFORE create_all is called
import models  # This ensures BookTable is registered with Base

engine = create_engine(DATABASE_URL, echo=True)

# Now that models have been imported, create the tables
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
