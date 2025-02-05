from pydantic import BaseModel

# 📌 Esquema para recibir parámetros en `/tendencias_diarias`
class FiltrosTendenciaDiaria(BaseModel):
    order: str = "asc"  # Orden de los datos
    n_ultimos_dias: int = 300  # Últimos 300 días por defecto

# 📌 Esquema para recibir parámetros en `/tendencias_mensuales`
class FiltrosTendenciaMensual(BaseModel):
    order: str = "asc"  # Orden de los datos
    n_ultimos_meses: int = 12  # Últimos 12 meses por defecto