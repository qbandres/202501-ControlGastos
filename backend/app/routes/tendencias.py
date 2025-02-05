from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.data_graficos import FiltrosGraficoFechaDia, FiltrosGraficoFechaMes
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from app.services.graficos_service import get_datos_fecha_dia, get_datos_fecha_mes

router = APIRouter()

@router.post("/tendencias_diarias")
def obtener_tendencias_diarias(filtros: FiltrosGraficoFechaDia, db: Session = Depends(get_db)):
    try:
        # 1. Obtener datos históricos
        data = get_datos_fecha_dia(filtros, db)
        df = pd.DataFrame(data)
        
        # 2. Calcular promedio móvil
        df['promedio'] = df['value'].rolling(window=7, min_periods=1).mean()  # Ventana de 7 días
        
        # 3. Preparar para regresión lineal
        df['fecha_num'] = np.arange(len(df))  # Convertir fechas a números
        X = df[['fecha_num']].values
        y = df['value'].values
        modelo = LinearRegression()
        modelo.fit(X, y)

        # 4. Proyección futura
        dias_futuros = np.arange(len(df), len(df) + 30).reshape(-1, 1)  # Próximos 30 días
        predicciones = modelo.predict(dias_futuros)
        fechas_futuras = pd.date_range(start=df['label'].iloc[-1], periods=31, freq='D')[1:]
        
        # 5. Combinar datos históricos con proyección
        forecast = [{'label': fecha.strftime('%Y-%m-%d'), 'value': None, 'promedio': None, 'forecast': float(pred)}
                    for fecha, pred in zip(fechas_futuras, predicciones)]
        resultado = df[['label', 'value', 'promedio']].to_dict(orient='records') + forecast
        
        # Asegurar que todas las entradas tengan las 4 columnas
        for item in resultado:
            if 'forecast' not in item:
                item['forecast'] = None
        
        return {"status": "success", "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular tendencia diaria: {str(e)}")

@router.post("/tendencias_mensuales")
def obtener_tendencias_mensuales(filtros: FiltrosGraficoFechaMes, db: Session = Depends(get_db)):
    try:
        # 1. Obtener datos históricos
        data = get_datos_fecha_mes(filtros, db)
        df = pd.DataFrame(data)
        
        # 2. Calcular promedio móvil
        df['promedio'] = df['value'].rolling(window=3, min_periods=1).mean()  # Ventana de 3 meses
        
        # 3. Preparar para regresión lineal
        df['mes_num'] = np.arange(len(df))  # Convertir meses a números
        X = df[['mes_num']].values
        y = df['value'].values
        modelo = LinearRegression()
        modelo.fit(X, y)

        # 4. Proyección futura
        meses_futuros = np.arange(len(df), len(df) + 6).reshape(-1, 1)  # Próximos 6 meses
        predicciones = modelo.predict(meses_futuros)
        meses_futuros_labels = pd.date_range(start=df['label'].iloc[-1], periods=7, freq='MS')[1:]
        
        # 5. Combinar datos históricos con proyección
        forecast = [{'label': mes.strftime('%Y-%m'), 'value': None, 'promedio': None, 'forecast': float(pred)}
                    for mes, pred in zip(meses_futuros_labels, predicciones)]
        resultado = df[['label', 'value', 'promedio']].to_dict(orient='records') + forecast
        
        # Asegurar que todas las entradas tengan las 4 columnas
        for item in resultado:
            if 'forecast' not in item:
                item['forecast'] = None
        
        return {"status": "success", "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular tendencia mensual: {str(e)}")