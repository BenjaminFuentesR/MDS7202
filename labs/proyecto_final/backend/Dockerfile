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
RUN mkdir backend
COPY . ./backend/
ENV PYTHONPATH=/app

# Se expone el puerto de FastAPI.
EXPOSE 8000

# Entrypoint para el entorno virtual de uv.
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
