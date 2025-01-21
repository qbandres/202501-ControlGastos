from fastapi import FastAPI
from app.routes.login import router as login_router
from app.routes.tablaGastos import router as gastos_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes import modificar
from app.routes import graficos

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia según la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas del login
app.include_router(login_router)
app.include_router(gastos_router)  # Asegúrate de que este router esté incluido
app.include_router(modificar.router, prefix="/modificar", tags=["modificar"])
app.include_router(graficos.router, prefix="/graficos", tags=["Graficos"])