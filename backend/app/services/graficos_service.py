from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from app.models.datagastos import ControlGastos
from app.schemas.data_graficos import FiltrosGraficoFechaDia, FiltrosGraficoFechaMes
from datetime import timedelta

def get_datos_fecha_dia(filtros: FiltrosGraficoFechaDia, db: Session):
    """
    Lógica para obtener datos diarios agrupados.
    """
    columnas_validas = {"fecha", "cantidad"}
    if filtros.x_column not in columnas_validas or filtros.y_column not in columnas_validas:
        raise ValueError("Las columnas especificadas no son válidas.")
    
    ultima_fecha = db.query(func.max(ControlGastos.fecha)).scalar()
    if not ultima_fecha:
        return []
    
    fecha_minima = ultima_fecha - timedelta(days=filtros.n_ultimos_dias - 1)
    order_by_column = desc(ControlGastos.fecha) if filtros.order == "desc" else asc(ControlGastos.fecha)

    resultados = (
        db.query(
            ControlGastos.fecha.label("x"),
            func.sum(getattr(ControlGastos, filtros.y_column)).label("y")
        )
        .filter(ControlGastos.fecha >= fecha_minima)
        .group_by(ControlGastos.fecha)
        .order_by(order_by_column)
        .limit(filtros.n_ultimos_dias)
        .all()
    )
    return [{"label": str(row.x), "value": row.y} for row in resultados]

def get_datos_fecha_mes(filtros: FiltrosGraficoFechaMes, db: Session):
    """
    Lógica para obtener datos mensuales agrupados.
    """
    order_by_column = desc("mes") if filtros.order == "desc" else asc("mes")

    resultados = (
        db.query(
            func.to_char(func.date_trunc("month", ControlGastos.fecha), "YYYY-MM").label("mes"),
            func.sum(getattr(ControlGastos, filtros.y_column)).label("total_cantidad")
        )
        .group_by("mes")
        .order_by(order_by_column)
        .limit(filtros.n_ultimos_meses)
        .all()
    )
    return [{"label": row.mes, "value": row.total_cantidad} for row in resultados]