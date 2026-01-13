import sys
import os

# Agregar el directorio actual al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database.connection import engine

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("\n✅ Conexión exitosa a Supabase!")
            print(f"Versión de DB: {connection.execute(text('SELECT version()')).scalar()}")
    except Exception as e:
        print("\n❌ Error al conectar a la base de datos:")
        print(e)

if __name__ == "__main__":
    test_connection()
