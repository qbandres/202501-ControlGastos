# Usamos una imagen ligera de Python 3.11
FROM python:3.11-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para iniciar la aplicación (0.0.0.0 es necesario para contenedores)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
