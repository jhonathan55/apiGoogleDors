# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements y luego instalar dependencias
COPY requirements.txt .

# Buenas prácticas: instalar solo lo necesario, limpiar cache
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Variable de entorno para evitar que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Comando por defecto para ejecutar el script
CMD ["python", "main.py"]
