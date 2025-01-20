from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.connection import get_db  # Usamos la función get_db definida en connection.py
from app.models.user import User

# Crear el enrutador para las rutas relacionadas con el login
router = APIRouter()

# Modelo para la solicitud del login
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint para autenticar usuarios.
    """
    # Buscar al usuario en la base de datos usando el username
    user = db.query(User).filter(User.username == request.username).first()

    # Verificar si el usuario existe y si la contraseña coincide
    if not user or user.password_hash != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    # Retornar una respuesta de éxito si las credenciales son válidas
    return {"message": "Login exitoso", "username": user.username}

#Probar con la terminal
# curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d '{"username": "Yovana", "password": "Yovanaperez"}'% 