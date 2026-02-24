from sqlalchemy.orm import Session
from models import Computer
from schemas import ComputerCreate



def create_computer(db: Session, computer: ComputerCreate):
    new_computer = Computer(**computer.dict())
    db.add(new_computer)
    db.commit()
    db.refresh(new_computer)
    return new_computer


def get_all_computers(db: Session):
    return db.query(Computer).all()


def get_product(db: Session, computer_id: int):
    return db.query(Computer).filter(Computer.id == computer_id).first()



def update_computer(db: Session, computer_id: int, computer: ComputerCreate):
    db_computer = db.query(Computer).filter(Computer.id == computer_id).first()
    if not db_computer:
        return None
    db_computer.brand = computer.brand
    db_computer.model = computer.model
    db_computer.price = computer.price
    db_computer.decscription = computer.description
    db.commit()
    db.refresh(db_computer)
    return db_computer

def delete_computer(db: Session, computer_id: int):
    db_computer = db.query(Computer).filter(Computer.id == computer_id).first()
    if not db_computer:
        return None
    db.delete(db_computer)
    db.commit()
    return db_computer

