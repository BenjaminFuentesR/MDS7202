# models.py


# Librerías.
from pydantic import BaseModel, Field


# Main.
class PredictionRequest(BaseModel):
    asunto: str = Field(..., description="Asunto del ticket")
    contenido: str = Field(..., description="Contenido detallado del ticket")
    canal: str = Field(..., description="Canal por el que llegó el ticket")
    categoria: str = Field(..., description="Categoría del problema")


class PredictionResponse(BaseModel):
    prioridad: str = Field(..., description="Nivel de prioridad predicho: Baja, Media, Alta, Crítica")
