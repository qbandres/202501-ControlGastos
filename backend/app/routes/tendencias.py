from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Modelos de respuesta
class TendenciaDiaria(BaseModel):
    fecha: str
    cantidad: float

class TendenciaMensual(BaseModel):
    mes: str
    cantidad: float

@router.get("/diarias", response_model=List[TendenciaDiaria])
def calcular_tendencia_diaria(db: Session = Depends(get_db)):
    """
    Calcula la tendencia diaria de los gastos utilizando regresión lineal.
    """
    try:
        # Consulta los datos
        datos = db.query(ControlGastos.fecha, func.sum(ControlGastos.cantidad)).group_by(ControlGastos.fecha).order_by(ControlGastos.fecha).all()
        if not datos:
            raise HTTPException(status_code=404, detail="No hay datos disponibles para calcular la tendencia diaria")

        # Crear DataFrame
        df = pd.DataFrame(datos, columns=["fecha", "cantidad"])
        df["fecha"] = pd.to_datetime(df["fecha"])  # Asegurar que las fechas sean de tipo datetime
        df["fecha_num"] = (df["fecha"] - df["fecha"].min()).dt.days

        # Regresión Lineal
        X = df[["fecha_num"]].values
        y = df["cantidad"].values
        modelo = LinearRegression()
        modelo.fit(X, y)

        # Predicción de los próximos 30 días
        ultimo_dia = df["fecha_num"].max()
        dias_futuros = np.arange(ultimo_dia + 1, ultimo_dia + 31).reshape(-1, 1)
        predicciones = modelo.predict(dias_futuros)

        # Formatear las fechas futuras
        fechas_futuras = [df["fecha"].min() + pd.Timedelta(days=int(dia)) for dia in dias_futuros.flatten()]
        resultado = [{"fecha": fecha.strftime("%Y-%m-%d"), "cantidad": float(cantidad)} for fecha, cantidad in zip(fechas_futuras, predicciones)]

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular tendencia diaria: {str(e)}")

@router.get("/mensuales", response_model=List[TendenciaMensual])
def calcular_tendencia_mensual(db: Session = Depends(get_db)):
    """
    Calcula la tendencia mensual de los gastos utilizando regresión lineal.
    """
    try:
        # Consulta agrupando por mes truncado
        datos = (
            db.query(
                func.date_trunc("month", ControlGastos.fecha).label("mes"),  # Alias "mes"
                func.sum(ControlGastos.cantidad).label("cantidad")
            )
            .group_by("mes")  # Agrupa por el alias "mes"
            .order_by("mes")  # Ordena por el alias "mes"
            .all()
        )

        if not datos:
            raise HTTPException(status_code=404, detail="No hay datos disponibles para calcular la tendencia mensual")

        # Crear DataFrame
        df = pd.DataFrame(datos, columns=["mes", "cantidad"])
        df["mes"] = pd.to_datetime(df["mes"])  # Asegurar que los meses sean de tipo datetime
        df["mes_num"] = np.arange(len(df))  # Crear índices para los meses

        # Regresión Lineal
        X = df[["mes_num"]].values
        y = df["cantidad"].values
        modelo = LinearRegression()
        modelo.fit(X, y)

        # Predicción de los próximos 12 meses
        ultimo_mes = df["mes_num"].max()
        meses_futuros = np.arange(ultimo_mes + 1, ultimo_mes + 13).reshape(-1, 1)
        predicciones = modelo.predict(meses_futuros)

        # Formatear los meses futuros
        meses_futuros_str = [
            (df["mes"].iloc[0] + pd.DateOffset(months=int(mes))).strftime("%Y-%m")
            for mes in meses_futuros.flatten()
        ]
        resultado = [{"mes": mes, "cantidad": float(cantidad)} for mes, cantidad in zip(meses_futuros_str, predicciones)]

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular tendencia mensual: {str(e)}")