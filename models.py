from sqlalchemy import Column, Integer, String
from database import Base

class BookTable(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    publication_year = Column(Integer)
    genre = Column(String(255))
    isbn = Column(String(50))
