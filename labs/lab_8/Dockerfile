# Imagen base ligera de Python
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor.
WORKDIR /app

# Se copia el archivo de requerimientos y se instalan dependencias.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Se copia el resto del código.
COPY . .

# Se expone el puerto 8000.
EXPOSE 8000

# Ejecutar API.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
