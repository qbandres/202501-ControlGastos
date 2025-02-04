from pydantic import BaseModel

# 📌 Esquema para recibir parámetros en `/datos_fecha_dia`
class FiltrosGraficoFechaDia(BaseModel):
    x_column: str  # Debe ser "fecha"
    y_column: str  # Ejemplo: "cantidad"
    n_ultimos_dias: int  # Número de días a extraer