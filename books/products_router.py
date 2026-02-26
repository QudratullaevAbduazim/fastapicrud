from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import BookCreate, BookResponse
import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_obj = crud.create_book(db, book)
    return {
        "message": "Kitob muvaffaqiyatli qo‘shildi",
        "data": new_obj
    }


@router.get("/", response_model=list[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)


@router.get("/{book_id}", response_model=BookResponse)
def get_one(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return db_book


@router.put("/{book_id}")
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    updated = crud.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return {
        "message": "Kitob muvaffaqiyatli yangilandi",
        "data": updated
    }


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return {
        "message": "Kitob muvaffaqiyatli o‘chirildi"
    }