# services.py


# Librerías.
import os

import requests

# Configuración.

# Se obtiene la URL desde la variable de ambiente. Si no, se usa la ruta local.
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/predict")


# Main.
def enviar_prediccion(asunto: str, contenido: str, canal: str, categoria: str) -> str:
    """
    Realiza una petición POST al endpoint de FastAPI para obtener la predicción del ticket.
    """

    params = {"asunto": asunto, "contenido": contenido, "canal": canal, "categoria": categoria}

    response = requests.post(BACKEND_URL, json=params)
    data = response.json()

    return data["prioridad"]
