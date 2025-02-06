from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from app.services.filters_data import apply_filters
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

router = APIRouter()

# 🟢 Modelo para recibir los filtros desde el frontend
class FiltrosGastos(BaseModel):
    usuario: Optional[str] = Field(None, description="Usuario específico para filtrar")
    clase: Optional[str] = Field(None, description="Clase específica para filtrar")
    rango_fecha_inicio: Optional[date] = Field(None, description="Fecha mínima")
    rango_fecha_fin: Optional[date] = Field(None, description="Fecha máxima")
    rango_cantidad_min: Optional[float] = Field(None, description="Cantidad mínima")
    rango_cantidad_max: Optional[float] = Field(None, description="Cantidad máxima")
    clase_in: Optional[List[str]] = Field(None, description="Lista de clases para filtrar")

# 🟢 Endpoint para obtener gastos filtrados
@router.post("/tabla-gastos")
def get_filtered_gastos(filters: FiltrosGastos, db: Session = Depends(get_db)):
    """
    Devuelve los registros filtrados de la tabla ControlGastos según los parámetros enviados
    junto con estadísticas como la suma total y la cantidad de registros.
    """
    try:
        # Base de la consulta
        query = db.query(ControlGastos)

        # Validar y aplicar filtros dinámicos
        if filters.rango_fecha_inicio and filters.rango_fecha_fin:
            if filters.rango_fecha_inicio > filters.rango_fecha_fin:
                raise HTTPException(status_code=400, detail="La fecha inicial no puede ser mayor que la fecha final.")
            query = query.filter(
                and_(
                    ControlGastos.fecha >= filters.rango_fecha_inicio,
                    ControlGastos.fecha <= filters.rango_fecha_fin
                )
            )

        if filters.rango_cantidad_min is not None and filters.rango_cantidad_max is not None:
            if filters.rango_cantidad_min > filters.rango_cantidad_max:
                raise HTTPException(status_code=400, detail="La cantidad mínima no puede ser mayor que la cantidad máxima.")
            query = query.filter(
                and_(
                    ControlGastos.cantidad >= filters.rango_cantidad_min,
                    ControlGastos.cantidad <= filters.rango_cantidad_max
                )
            )

        if filters.usuario:
            query = query.filter(ControlGastos.usuario == filters.usuario)
        if filters.clase:
            query = query.filter(ControlGastos.clase == filters.clase)
        if filters.clase_in:
            query = query.filter(ControlGastos.clase.in_(filters.clase_in))

        # Ordenar por fecha descendente
        query = query.order_by(ControlGastos.fecha.desc())

        # Obtener todos los resultados para estadísticas
        all_results = query.all()
        total_cantidad = sum(gasto.cantidad for gasto in all_results)  # Suma total
        total_registros = len(all_results)  # Cantidad de registros

        # Limitar a 100 resultados para la tabla
        results = all_results[:100]

        # Verificar si hay resultados
        if not results:
            return {
                "status": "success",
                "message": "No se encontraron registros con los filtros aplicados.",
                "data": [],
                "total_cantidad": 0,
                "total_registros": 0
            }

        # Formatear la respuesta
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
            "total_cantidad": total_cantidad,
            "total_registros": total_registros
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al filtrar datos: {str(e)}")


# 🟢 Endpoint para obtener los últimos 20 gastos
@router.get("/tabla-gastos")
def get_last_20_gastos(db: Session = Depends(get_db)):
    """
    Devuelve los últimos 20 gastos según la fecha de ingreso, junto con estadísticas.
    """
    try:
        gastos = (
            db.query(ControlGastos)
            .order_by(ControlGastos.fecha.desc())
            .limit(20)
            .all()
        )

        # Verificar si hay resultados
        if not gastos:
            return {
                "status": "success",
                "message": "No hay datos disponibles.",
                "data": [],
                "total_cantidad": 0,
                "total_registros": 0
            }

        # Calcular estadísticas
        total_cantidad = sum(gasto.cantidad for gasto in gastos)  # Suma total
        total_registros = len(gastos)  # Cantidad de registros

        # Formatear la respuesta
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
            "total_cantidad": total_cantidad,
            "total_registros": total_registros
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")