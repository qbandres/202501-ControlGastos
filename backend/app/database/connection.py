from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  # Importa declarative_base para los modelos
from app.config import settings

# URL de la base de datos
DATABASE_URL = (
    f"postgresql+psycopg://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear la clase base para los modelos ORM
Base = declarative_base()

# Configurar el manejador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener una sesión de base de datos
def get_db():
    """
    Proporciona una sesión de base de datos para usar en las rutas.
    Cierra la sesión automáticamente después de cada solicitud.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()