from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import crud
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/categories/", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_category(db, category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category name already exists")


@app.get("/categories/", response_model=list[schemas.CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.post("/books/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if not db.query(models.Category).filter(models.Category.id == book.category_id).first():
        raise HTTPException(status_code=400, detail="Category does not exist")
    try:
        return crud.create_book(db, book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="ISBN already exists")


@app.get("/books/", response_model=list[schemas.BookResponse])
def read_books(category_id: int | None = None, db: Session = Depends(get_db)):
    if category_id is not None and not db.query(models.Category).filter(models.Category.id == category_id).first():
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.get_books(db, category_id)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, data: schemas.BookCreate, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not db.query(models.Category).filter(models.Category.id == data.category_id).first():
        raise HTTPException(status_code=400, detail="Category does not exist")
    try:
        return crud.update_book(db, book, data.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="ISBN already exists")


@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, book)
    return {"message": "Book deleted successfully"}
