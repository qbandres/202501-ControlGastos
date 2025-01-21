from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from typing import Optional, List, Dict

router = APIRouter()

# Modelo para validar los datos entrantes
class XYChartRequest(BaseModel):
    x_axis: str
    y_axis: str
    filters: Optional[Dict] = None  # Filtros opcionales

@router.post("/x-y")
def get_xy_data(request: XYChartRequest, db: Session = Depends(get_db)):
    try:
        # Base de la consulta
        query = db.query(ControlGastos)

        # Aplicar filtros si existen
        if request.filters:
            if "fecha" in request.filters:
                fecha_filtro = request.filters["fecha"]
                if "start" in fecha_filtro:
                    query = query.filter(ControlGastos.fecha >= fecha_filtro["start"])
                if "end" in fecha_filtro:
                    query = query.filter(ControlGastos.fecha <= fecha_filtro["end"])

            if "clase" in request.filters:
                query = query.filter(ControlGastos.clase.in_(request.filters["clase"]))

        # Obtener datos de las columnas X e Y
        data = query.with_entities(
            getattr(ControlGastos, request.x_axis),
            getattr(ControlGastos, request.y_axis),
        ).all()

        # Formatear los datos para el gráfico
        formatted_data = [{"x": row[0], "y": row[1]} for row in data]

        return {"status": "success", "data": formatted_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar datos: {str(e)}")