from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.login import router as login_router
from app.routes.tablaGastos import router as gastos_router
from app.routes import modificar, graficos, tendencias
from app.routes.resumen_gastos import router as resumen_gastos_router
from app.routes import resumen_gastos
from app.routes.agregarGastos import router as agregar_gasto_router

app = FastAPI()

# Configurar CORS para producción y desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://two02501-controlgastos.onrender.com"],  # Cambia según la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas del login, gastos, modificar, gráficos y tendencias
app.include_router(login_router)
app.include_router(gastos_router)
app.include_router(modificar.router, prefix="/modificar", tags=["Modificar"])
app.include_router(graficos.router, prefix="/graficos", tags=["Gráficos"])
app.include_router(tendencias.router, prefix="/tendencias", tags=["Tendencias"])
app.include_router(resumen_gastos.router, prefix="/resumen-gastos", tags=["Resumen Gastos"])

# Registra las rutas para agregar gasto
app.include_router(agregar_gasto_router)