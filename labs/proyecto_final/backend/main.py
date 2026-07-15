# main.py


# Librerías.
from fastapi import FastAPI, HTTPException
from backend.models import PredictionRequest, PredictionResponse

from backend.generate_prediction import generate_prediction




# Configuración.
app = FastAPI(
    title = "API de Priorización de Tickets",
    description = "API para predecir la prioridad de los tickets de soporte usando MLP con Embeddings.")
@app.post("/predict", response_model = PredictionResponse)




# Main.
def predict_priority(request: PredictionRequest):
    try:
        
        # Se extraen los datos validados por Pydantic y se pasan a la función.
        resultado = generate_prediction(
            asunto = request.asunto,
            contenido = request.contenido,
            canal = request.canal,
            categoria = request.categoria)

        # Se retorna la predicción según pydantic.
        return PredictionResponse(prioridad = resultado)

    except Exception as e:
        raise HTTPException(
            status_code = 500, # Porque es un error interno.
            detail = f"Error al intentar generar la predicción: {str(e)}")