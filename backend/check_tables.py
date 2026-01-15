from sqlalchemy import create_engine, inspect
from app.config import settings
import os

# Construct the database URL
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
inspector = inspect(engine)

print("Tables in the database:")
for table_name in inspector.get_table_names():
    print(f"- {table_name}")
