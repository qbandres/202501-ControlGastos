import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # Esto ya es una lista,
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
from app.routes import data_graficos  # Importamos el nuevo endpoint

app.include_router(login_router)
app.include_router(gastos_router)
app.include_router(modificar.router, prefix="/modificar", tags=["Modificar"])
app.include_router(graficos.router, prefix="/graficos", tags=["Gráficos"])
app.include_router(tendencias.router, prefix="/tendencias", tags=["Tendencias"])
app.include_router(resumen_gastos_router, prefix="/resumen-gastos", tags=["Resumen Gastos"])
app.include_router(agregar_gasto_router)
app.include_router(data_graficos.router, prefix="/graficos_dinamicos",tags=["Gráficos Dinámicos"])

@app.get("/")
def read_root():
    return {"message": "API de Control de Gastos funcionando correctamente 🚀"}