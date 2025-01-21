from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, Date, cast
from app.database.connection import get_db
from app.models.datagastos import ControlGastos

router = APIRouter()

class XYDataRequest(BaseModel):
    x_axis: str
    y_axis: str
    filters: dict

@router.post("/x-y")
def get_xy_data(data: XYDataRequest, db: Session = Depends(get_db)):
    try:
        query = db.query(
            getattr(ControlGastos, data.x_axis).label("x"),  # Eje X
            func.sum(getattr(ControlGastos, data.y_axis)).label("y")  # Sumar valores del eje Y
        )

        # Aplicar filtros
        filters = data.filters
        if "fecha" in filters:
            if "start" in filters["fecha"]:
                query = query.filter(
                    ControlGastos.fecha >= cast(filters["fecha"]["start"], Date)
                )
            if "end" in filters["fecha"]:
                query = query.filter(
                    ControlGastos.fecha <= cast(filters["fecha"]["end"], Date)
                )

        # Agrupar por el eje X y ordenar
        query = query.group_by(getattr(ControlGastos, data.x_axis)).order_by(getattr(ControlGastos, data.x_axis))

        # Obtener datos agrupados
        data_points = query.all()

        # Formatear datos para el gráfico
        formatted_data = [{"x": row.x, "y": row.y} for row in data_points]

        return {"status": "success", "data": formatted_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar datos: {str(e)}")