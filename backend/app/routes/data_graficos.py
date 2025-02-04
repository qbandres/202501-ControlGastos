from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from datetime import timedelta,datetime
from sqlalchemy import func, desc  # Asegúrate de importar 'desc'
from app.schemas.graficos_dinamicos import FiltrosGraficoFechaDia  # Importamos el esquema desde schemas


router = APIRouter()

# 🟢 Endpoint para obtener datos agrupados por día
@router.post("/datos_fecha_dia")
def get_datos_fecha_dia(filtros: FiltrosGraficoFechaDia, db: Session = Depends(get_db)):
    columnas_validas = {"fecha", "cantidad"}
    if filtros.x_column not in columnas_validas or filtros.y_column not in columnas_validas:
        raise HTTPException(status_code=400, detail="Las columnas especificadas no son válidas.")
    ultima_fecha = db.query(func.max(ControlGastos.fecha)).scalar()
    if not ultima_fecha:
        raise HTTPException(status_code=404, detail="No hay datos en la base de datos.")
    fecha_minima = ultima_fecha - timedelta(days=filtros.n_ultimos_dias - 1)
    resultados = (
        db.query(
            ControlGastos.fecha.label("x"),
            func.sum(getattr(ControlGastos, filtros.y_column)).label("y")
        )
        .filter(ControlGastos.fecha >= fecha_minima)
        .group_by(ControlGastos.fecha)
        .order_by(ControlGastos.fecha.desc())
        .limit(filtros.n_ultimos_dias)
        .all()
    )
    response = [{"label": str(row.x), "value": row.y} for row in resultados]
    return {"status": "success", "data": response}

# 🟢 Endpoint para obtener datos agregados por mes usando Pandas
@router.post("/datos_fecha_mes")
def get_datos_fecha_mes(db: Session = Depends(get_db)):
    """
    📌 **Función para obtener datos agregados por mes**
    
    **Proceso:**
    - Agrupa los datos **por mes** (`YYYY-MM`).
    - Suma los valores de `cantidad` para cada mes.
    - Ordena **de manera descendente** por mes.

    **Salida esperada (JSON para el frontend):**
    ```json
    {
      "status": "success",
      "data": [
        {"label": "2025-02", "value": 2500.0},
        {"label": "2025-01", "value": 3809.77},
        {"label": "2024-12", "value": 35189.33}
      ]
    }
    ```
    """
    try:
        # 🔹 Consulta optimizada para PostgreSQL
        resultados = (
            db.query(
                func.to_char(func.date_trunc("month", ControlGastos.fecha), "YYYY-MM").label("mes"),
                func.sum(ControlGastos.cantidad).label("total_cantidad")
            )
            .group_by("mes")  # Agrupa por el campo "mes"
            .order_by(desc("mes"))  # Ordena de manera descendente por "mes"
            .all()
        )

        # 🔹 Transformar el resultado en formato JSON
        response = [{"label": row.mes, "value": row.total_cantidad} for row in resultados]

        return {"status": "success", "data": response}

    except Exception as e:
        # 🔹 Captura cualquier excepción y devuelve un error 500
        raise HTTPException(status_code=500, detail=f"Error al obtener datos por mes: {str(e)}")