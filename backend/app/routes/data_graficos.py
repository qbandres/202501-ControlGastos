from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from datetime import timedelta,datetime
from sqlalchemy import func, desc, asc  # Asegúrate de importar 'desc'
from app.schemas.graficos_dinamicos import FiltrosGraficoFechaDia, FiltrosGraficoFechaMes # Importamos el esquema desde schemas


router = APIRouter()

# 🟢 Endpoint optimizado para obtener datos agrupados por día
@router.post("/datos_fecha_dia")
def get_datos_fecha_dia(
    filtros: FiltrosGraficoFechaDia = FiltrosGraficoFechaDia(),  # Aplica valores por defecto
    db: Session = Depends(get_db)
):
    """
    📌 Obtiene los últimos `n_ultimos_dias` días de gastos agrupados y ordenados según `order`.
    """
    try:
        columnas_validas = {"fecha", "cantidad"}
        if filtros.x_column not in columnas_validas or filtros.y_column not in columnas_validas:
            raise HTTPException(status_code=400, detail="Las columnas especificadas no son válidas.")

        # 🔹 Obtener la fecha máxima disponible en la base de datos
        ultima_fecha = db.query(func.max(ControlGastos.fecha)).scalar()
        if not ultima_fecha:
            raise HTTPException(status_code=404, detail="No hay datos en la base de datos.")

        # 🔹 Calcular la fecha mínima basada en `n_ultimos_dias`
        fecha_minima = ultima_fecha - timedelta(days=filtros.n_ultimos_dias - 1)

        # 🔹 Definir el orden dinámicamente según `order`
        order_by_column = desc(ControlGastos.fecha) if filtros.order == "desc" else asc(ControlGastos.fecha)

        # 🔹 Consulta optimizada
        resultados = (
            db.query(
                ControlGastos.fecha.label("x"),
                func.sum(getattr(ControlGastos, filtros.y_column)).label("y")
            )
            .filter(ControlGastos.fecha >= fecha_minima)
            .group_by(ControlGastos.fecha)
            .order_by(order_by_column)  # Orden dinámico
            .limit(filtros.n_ultimos_dias)
            .all()
        )

        # 🔹 Formateo de la respuesta JSON
        response = [{"label": str(row.x), "value": row.y} for row in resultados]

        return {"status": "success", "data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos por día: {str(e)}")

# 🟢 Endpoint optimizado para obtener datos agregados por mes
@router.post("/datos_fecha_mes")
def get_datos_fecha_mes(
    filtros: FiltrosGraficoFechaMes = FiltrosGraficoFechaMes(),  # Aplica valores por defecto
    db: Session = Depends(get_db)
):
    """
    📌 Obtiene los últimos `n_ultimos_meses` meses de gastos agrupados y ordenados según `order`.
    """
    try:
        # 🔹 Definir el orden dinámicamente según `order`
        order_by_column = desc("mes") if filtros.order == "desc" else asc("mes")

        # 🔹 Consulta optimizada para PostgreSQL
        resultados = (
            db.query(
                func.to_char(func.date_trunc("month", ControlGastos.fecha), "YYYY-MM").label("mes"),
                func.sum(getattr(ControlGastos, filtros.y_column)).label("total_cantidad")
            )
            .group_by("mes")  # Agrupa por el campo "mes"
            .order_by(order_by_column)  # Orden dinámico
            .limit(filtros.n_ultimos_meses)  # Aplica el límite de meses
            .all()
        )

        # 🔹 Transformar el resultado en formato JSON
        response = [{"label": row.mes, "value": row.total_cantidad} for row in resultados]

        return {"status": "success", "data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos por mes: {str(e)}")