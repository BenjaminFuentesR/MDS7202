import pickle

import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

with open("models/best_model.pkl", "rb") as f:
    model = pickle.load(f)


class WaterMeasurement(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float


@app.get("/")
def home():
    return {
        "modelo": "XGBoost clasificador de potabilidad del agua",
        "problema": "Predecir si el agua es potable (1) o no potable (0) a partir de mediciones químicas",
        "input": "9 variables numéricas: ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity",
        "output": "potabilidad: 0 (no potable) o 1 (potable)",
    }


@app.post("/potabilidad/")
def predecir_potabilidad(medicion: WaterMeasurement):
    datos = np.array(
        [
            [
                medicion.ph,
                medicion.Hardness,
                medicion.Solids,
                medicion.Chloramines,
                medicion.Sulfate,
                medicion.Conductivity,
                medicion.Organic_carbon,
                medicion.Trihalomethanes,
                medicion.Turbidity,
            ]
        ]
    )
    prediccion = model.predict(datos)
    return {"potabilidad": int(prediccion[0])}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
