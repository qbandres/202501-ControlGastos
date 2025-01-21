from sqlalchemy.orm import Session
from app.models.datagastos import ControlGastos

def delete_gasto(id: int, db: Session):
    gasto = db.query(ControlGastos).filter(ControlGastos.id == id).first()
    if not gasto:
        return False
    db.delete(gasto)
    db.commit()
    return True