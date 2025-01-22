from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Modelo de datos para agregar un gasto
class GastoBase(BaseModel):
    usuario: str
    clase: str
    asignacion: str
    cantidad: float
    tipo: str
    locacion: str
    fecha: str
    observaciones: str
    metodo: str

# Ruta POST para agregar un gasto
@router.post("/agregar-gasto")
def agregar_gasto(gasto: GastoBase, db: Session = Depends(get_db)):
    try:
        # Crear una nueva instancia de ControlGastos
        nuevo_gasto = ControlGastos(
            usuario=gasto.usuario,
            clase=gasto.clase,
            asignacion=gasto.asignacion,
            cantidad=gasto.cantidad,
            tipo=gasto.tipo,
            locacion=gasto.locacion,
            fecha=datetime.strptime(gasto.fecha, "%Y-%m-%d"),
            observaciones=gasto.observaciones,
            metodo=gasto.metodo
        )

        # Agregar el gasto a la base de datos
        db.add(nuevo_gasto)
        db.commit()

        # Confirmar que el gasto se ha guardado
        db.refresh(nuevo_gasto)
        return {"message": "Gasto agregado exitosamente", "gasto": nuevo_gasto}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar el gasto: {str(e)}")