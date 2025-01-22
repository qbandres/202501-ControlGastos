from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.models.datagastos import ControlGastos
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

# Modelo Pydantic para los datos de tendencia mensual
class TendenciaMensual(BaseModel):
    mes: str
    total_gastos: float

@router.get("/gastos-ultimos-7-dias", response_model=dict)
def obtener_gastos_ultimos_7_dias(db: Session = Depends(get_db)):
    try:
        # Fecha límite para los últimos 7 días
        fecha_limite = datetime.now() - timedelta(days=7)
        print(f"Fecha límite para los últimos 7 días: {fecha_limite}")

        # Obtener los gastos de los últimos 7 días
        datos = (
            db.query(
                ControlGastos.fecha,
                func.sum(ControlGastos.cantidad).label("total_gastos")
            )
            .filter(ControlGastos.fecha >= fecha_limite)
            .group_by(ControlGastos.fecha)
            .order_by(ControlGastos.fecha)
            .all()
        )

        # Si no hay datos, devolver un valor estándar (0.0)
        if not datos:
            return {"status": "success", "data": [{"fecha": "No disponible", "total_gastos": 0.0}]}

        # Formatear la respuesta para el frontend
        resultado = [{"fecha": gasto.fecha.strftime("%Y-%m-%d"), "total_gastos": gasto.total_gastos} for gasto in datos]

        return {"status": "success", "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los gastos de los últimos 7 días: {str(e)}")

@router.get("/gastos-ultimos-3-meses", response_model=List[TendenciaMensual])
def obtener_gastos_ultimos_3_meses(db: Session = Depends(get_db)):
    try:
        # Definir el límite de fecha para los últimos 3 meses
        fecha_limite = datetime.now() - timedelta(days=90)
        print(f"Fecha límite para los últimos 3 meses: {fecha_limite}")

        # Obtener los gastos de los últimos 3 meses sin truncar las fechas
        datos = (
            db.query(
                ControlGastos.fecha,
                func.sum(ControlGastos.cantidad).label("total_gastos")
            )
            .filter(ControlGastos.fecha >= fecha_limite)
            .group_by(ControlGastos.fecha)  # Agrupar por la fecha completa
            .order_by(ControlGastos.fecha)  # Ordenar por la fecha
            .all()
        )

        # Si no hay datos, retornar un mensaje adecuado
        if not datos:
            print("No se encontraron datos para los últimos 3 meses")
            return [{"mes": "No disponible", "total_gastos": 0.0}]
        
        # Agrupar y truncar las fechas en el backend
        resultado = {}
        for fecha, total_gastos in datos:
            mes = fecha.strftime("%Y-%m")  # Truncamos la fecha para obtener solo el mes y el año
            if mes in resultado:
                resultado[mes] += total_gastos  # Sumar los gastos si ya existe el mes
            else:
                resultado[mes] = total_gastos  # Crear el mes si no existe

        # Convertir el resultado en una lista de diccionarios
        resultado_final = [{"mes": mes, "total_gastos": total} for mes, total in resultado.items()]

        print(f"Resultado final: {resultado_final}")

        return resultado_final
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener los gastos de los últimos 3 meses: {str(e)}")