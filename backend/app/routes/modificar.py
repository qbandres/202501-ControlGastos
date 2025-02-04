from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from app.services.filters_data import apply_filters

router = APIRouter()

@router.post("/")
def get_filtered_gastos(filters: dict, db: Session = Depends(get_db)):
    query = db.query(ControlGastos)
    query = apply_filters(query, filters)
    gastos = query.limit(20).all()
    query = query.order_by(ControlGastos.fecha.desc())
    return {"status": "success", "data": [g.to_dict() for g in gastos]}

@router.put("/{id}")
def update_gasto(id: int, gasto_data: dict, db: Session = Depends(get_db)):
    gasto = db.query(ControlGastos).filter(ControlGastos.id == id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    for key, value in gasto_data.items():
        setattr(gasto, key, value)
    db.commit()
    return {"status": "success", "message": "Gasto modificado exitosamente"}

@router.delete("/{id}")
def delete_gasto(id: int, db: Session = Depends(get_db)):
    gasto = db.query(ControlGastos).filter(ControlGastos.id == id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    db.delete(gasto)
    db.commit()
    return {"status": "success", "message": "Gasto eliminado exitosamente"}