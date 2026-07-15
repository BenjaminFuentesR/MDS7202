FROM python:3.12-slim

# Se define el directorio.
WORKDIR /app

# Se instala uv.
RUN pip install uv

# Se copian los archivos dependencias.
COPY pyproject.toml uv.lock ./

# Se sincronizan las dependencias.
RUN uv sync --frozen


# Se copia el resto del código.
RUN mkdir frontend
COPY . ./frontend/
ENV PYTHONPATH=/app

# Se expone el puerto de la app.
EXPOSE 7860

# Entrypoint para el entorno virtual de uv.
CMD ["uv", "run", "python", "app.py"]
