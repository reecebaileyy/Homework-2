from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import BookTable
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Pydantic schemas
class BookBase(BaseModel):
    title: str
    author: str
    publication_year: int
    genre: str = ""
    isbn: str = ""

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True

@router.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookTable(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/books", response_model=List[Book])
def read_books(db: Session = Depends(get_db)):
    return db.query(BookTable).all()

@router.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookTable).filter(BookTable.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(BookTable).filter(BookTable.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookTable).filter(BookTable.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted successfully"}
