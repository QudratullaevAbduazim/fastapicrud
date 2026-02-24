from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ComputerCreate, ComputerResponse
import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_computer(computer: ComputerCreate, db: Session = Depends(get_db)):
    new_obj = crud.create_computer(db, computer)
    return {
        "message": "Maxsulot muvaffaqiyatli qo‘shildi",
        "data": new_obj
    }


@router.get("/", response_model=list[ComputerResponse])
def get_all_computers(db: Session = Depends(get_db)):
    return crud.get_all_computers(db)


@router.get("/{computer_id}", response_model=ComputerResponse)
def get_one(computer_id: int, db: Session = Depends(get_db)):
    db_computer = crud.get_product(db, computer_id)
    if not db_computer:
        raise HTTPException(status_code=404, detail="Maxsulot topilmadi")
    return db_computer


@router.put("/{computer_id}")
def update_computer(computer_id: int, computer: ComputerCreate, db: Session = Depends(get_db)):
    updated = crud.update_computer(db, computer_id, computer)
    if not updated:
        raise HTTPException(status_code=404, detail="Maxsulot topilmadi")
    return {
        "message": "Maxsulot muvaffaqiyatli yangilandi",
        "data": updated
    }


@router.delete("/{computer_id}")
def delete_computer(computer_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_computer(db, computer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Maxsulot topilmadi")
    return {
        "message": "Maxsulot muvaffaqiyatli o‘chirildi"
    }