from pydantic import BaseModel
from typing import Optional

# 📌 Esquema actualizado para `/datos_fecha_dia`
class FiltrosGraficoFechaDia(BaseModel):
    x_column: Optional[str] = "fecha"  # Columna X (siempre será "fecha")
    y_column: Optional[str] = "cantidad"  # Columna Y (por defecto "cantidad")
    n_ultimos_dias: Optional[int] = 10  # Número de días a extraer (por defecto 10)
    order: Optional[str] = "desc"  # Orden por defecto "desc"

# 📌 Esquema actualizado para `/datos_fecha_mes`
class FiltrosGraficoFechaMes(BaseModel):
    x_column: Optional[str] = "mes"  # Columna X por defecto será "mes"
    y_column: Optional[str] = "cantidad"  # Columna Y por defecto será "cantidad"
    n_ultimos_meses: Optional[int] = 6  # Últimos 6 meses por defecto
    order: Optional[str] = "desc"  # Orden descendente por defecto