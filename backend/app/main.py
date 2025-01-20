from fastapi import FastAPI
from app.routes.login import router as login_router

app = FastAPI()

# Incluir las rutas del login
app.include_router(login_router)