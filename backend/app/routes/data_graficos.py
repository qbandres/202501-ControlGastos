from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.data_graficos import FiltrosGraficoFechaDia, FiltrosGraficoFechaMes
from app.services.graficos_service import get_datos_fecha_dia, get_datos_fecha_mes  # Cambiamos las importaciones

router = APIRouter()

@router.post("/datos_fecha_dia")
def datos_fecha_dia(filtros: FiltrosGraficoFechaDia, db: Session = Depends(get_db)):
    try:
        return {"status": "success", "data": get_datos_fecha_dia(filtros, db)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos diarios: {str(e)}")

@router.post("/datos_fecha_mes")
def datos_fecha_mes(filtros: FiltrosGraficoFechaMes, db: Session = Depends(get_db)):
    try:
        return {"status": "success", "data": get_datos_fecha_mes(filtros, db)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos mensuales: {str(e)}")