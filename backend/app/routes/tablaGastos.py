from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from app.services.filters_data import apply_filters
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

router = APIRouter()





class FiltrosGastos(BaseModel):
    usuario: Optional[str] = None
    clase: Optional[str] = None
    rango_fecha_inicio: Optional[date] = None  # Cambiado a tipo `date`
    rango_fecha_fin: Optional[date] = None  # Cambiado a tipo `date`
    clase_in: Optional[List[str]] = None
    rango_cantidad_min: Optional[float] = None
    rango_cantidad_max: Optional[float] = None


@router.post("/tabla-gastos")
def get_filtered_gastos(filters: FiltrosGastos, db: Session = Depends(get_db)):
    """
    Devuelve los registros filtrados de la tabla ControlGastos.
    Si no se envían filtros, devuelve todos los registros.
    """
    try:
        # Base de la consulta
        query = db.query(ControlGastos)

        # Convierte los filtros a un diccionario y aplica filtros dinámicos
        filtros_dict = filters.dict(exclude_unset=True)
        query = apply_filters(query, filtros_dict)


        # Ordenar por fecha descendente
        query = query.order_by(ControlGastos.fecha.desc())

        # Ejecuta la consulta
        results = query.all()

        # Devuelve los resultados en formato JSON
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
                for gasto in results
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al filtrar datos: {str(e)}")


@router.get("/tabla-gastos")
def get_last_20_gastos(db: Session = Depends(get_db)):
    """
    Devuelve los últimos 20 gastos según la fecha de ingreso.
    """
    try:
        gastos = (
            db.query(ControlGastos)
            .order_by(ControlGastos.fecha.desc())
            .limit(20)
            .all()
        )

        # Devuelve los resultados en formato JSON
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")