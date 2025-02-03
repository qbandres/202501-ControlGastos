import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Valor por defecto para desarrollo que incluye localhost.
default_origins = "http://localhost:5173"
# Si se define la variable de entorno ALLOWED_ORIGINS, se utilizará ese valor; 
# de lo contrario, se usará el valor por defecto.
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", default_origins)
allowed_origins = allowed_origins_str.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de la aplicación
from app.routes.login import router as login_router
from app.routes.tablaGastos import router as gastos_router
from app.routes import modificar, graficos, tendencias
from app.routes.resumen_gastos import router as resumen_gastos_router
from app.routes.agregarGastos import router as agregar_gasto_router

app.include_router(login_router)
app.include_router(gastos_router)
app.include_router(modificar.router, prefix="/modificar", tags=["Modificar"])
app.include_router(graficos.router, prefix="/graficos", tags=["Gráficos"])
app.include_router(tendencias.router, prefix="/tendencias", tags=["Tendencias"])
app.include_router(resumen_gastos_router, prefix="/resumen-gastos", tags=["Resumen Gastos"])
app.include_router(agregar_gasto_router)