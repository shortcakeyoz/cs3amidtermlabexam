from sqlalchemy.orm import Session
from models import Category, Book
from schemas import CategoryCreate, BookCreate


def create_category(db: Session, data: CategoryCreate):
    category = Category(name=data.name, description=data.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session):
    return db.query(Category).all()


def create_book(db: Session, data: BookCreate):
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session, category_id: int | None = None):
    query = db.query(Book)
    if category_id is not None:
        query = query.filter(Book.category_id == category_id)
    return query.all()


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book: Book, data: dict):
    for key, value in data.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book):
    db.delete(book)
    db.commit()
