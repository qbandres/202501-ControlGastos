from sqlalchemy import Column, Integer, String  # Importar las clases necesarias de SQLAlchemy para definir el modelo
from app.database.connection import Base  # Importar la clase base desde la conexión, que se utiliza para definir modelos ORM

# Definición del modelo ORM para la tabla "users"
class User(Base):
    __tablename__ = "users"  # Nombre de la tabla en la base de datos

    # Definir las columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False) # La columna "username" es de tipo string, debe ser única (no se pueden repetir valores) y no puede ser nula
    password_hash = Column(String, nullable=False)