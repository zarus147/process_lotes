# Usamos una imagen base de Python
FROM python:3.10-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo requirements.txt (que está en la raíz de fastapi/) dentro del contenedor
COPY requirements.txt /app/

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos los archivos de la aplicación dentro del contenedor
COPY ./app /app/app

# Exponemos el puerto que usaremos
EXPOSE 8000

# Ejecutamos FastAPI usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
