from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.datagastos import ControlGastos

router = APIRouter()

@router.get("/tabla-gastos")
def get_gastos_for_table(db: Session = Depends(get_db)):
    """
    Devuelve todos los gastos en formato adecuado para el componente de tabla.
    """
    try:
        gastos = db.query(ControlGastos).all()
        return {
            "status": "success",
            "data": [
                {
                    "id": gasto.id,
                    "usuario": gasto.usuario,   
                    "clase": gasto.clase,
                    "asignacion": gasto.asignacion,
                    "cantidad": gasto.cantidad,
                    "tipo": gasto.tipo,
                    "locacion": gasto.locacion,
                    "fecha": gasto.fecha.isoformat(),  # Serializa la fecha
                    "observaciones": gasto.observaciones,
                    "metodo": gasto.metodo,
                }
                for gasto in gastos
            ],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}