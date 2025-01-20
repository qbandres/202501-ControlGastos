from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.connection import get_db
from app.models.datagastos import ControlGastos

router = APIRouter()

@router.get("/tabla-gastos")
def get_last_20_gastos(db: Session = Depends(get_db)):
    """
    Devuelve los últimos 20 gastos según la fecha de ingreso (f_ingreso).
    """
    try:
        gastos = (
            db.query(ControlGastos)
            .order_by(ControlGastos.f_ingreso.desc())  # Ordenar por fecha descendente
            .limit(20)  # Limitar a los últimos 20 registros
            .all()
        )
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
                    "fecha": gasto.fecha.isoformat(),
                    "observaciones": gasto.observaciones,
                    "metodo": gasto.metodo,
                }
                for gasto in gastos
            ],
        }
    except SQLAlchemyError as e:
        return {"status": "error", "message": "Error en la base de datos", "details": str(e)}
    except Exception as e:
        return {"status": "error", "message": "Error desconocido", "details": str(e)}