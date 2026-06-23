# Escribe aquí tu código (copia el template y completa los TODOs)

from pathlib import Path
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


DATA_DIR = Path("/root/airflow/data") 
OUTPUT_PATH = Path("/tmp/spotify_data.parquet")

PARAM_COLS = [
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "tempo",
    "duration_ms",
    "year",
]


# ── Funciones auxiliares (dadas) ─────────────────────────────────────────────


def load_batch(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def load_all_parallel(data_dir: Path, n_batches: int = 5) -> pd.DataFrame:
    paths = sorted(data_dir.glob("*.parquet"))[:n_batches]
    with ThreadPoolExecutor(max_workers=None) as executor:
        dfs = list(executor.map(load_batch, [str(p) for p in paths]))
    return pd.concat(dfs, ignore_index=True)


def build_pipeline(n_jobs: int = -1) -> Pipeline:
    return Pipeline(
        [
            (
                "column_transformer",
                ColumnTransformer(
                    [
                        ("ohe", OneHotEncoder(handle_unknown="ignore"), ["key", "mode", "genre"]),
                        ("numerical", "passthrough", PARAM_COLS),
                    ]
                ),
            ),
            ("random_forest", RandomForestRegressor(n_jobs=n_jobs, random_state=42)),
        ]
    )


# ── Funciones de las tareas de Airflow ───────────────────────────────────────

def task_load_data_fn(**context):
    """
    Carga 5 batches de datos en paralelo y guarda el resultado en disco.
    TODO: implementa esta función.
    - Usa load_all_parallel para cargar los datos.
    - Guarda el DataFrame resultante en OUTPUT_PATH (formato parquet).
    - Usa XCom para pasar la ruta del archivo a la siguiente tarea.
    """

    # Se cargan 5 batches de datos en paralelo.
    df = load_all_parallel(DATA_DIR, n_batches = 5)

    # Se guardan los archivos en formato parquet.
    df.to_parquet(OUTPUT_PATH, index = False)

    # Se usa XCom para pasar la ruta del archivo.
    context['ti'].xcom_push(key = 'file_path', value = str(OUTPUT_PATH))


def task_train_model_fn(**context):
    """
    Carga los datos desde disco y entrena el pipeline.
    TODO: implementa esta función.
    - Recupera la ruta del archivo desde XCom.
    - Lee el DataFrame desde esa ruta.
    - Prepara X e y, realiza el split 80/20.
    - Entrena build_pipeline(n_jobs=-1).
    - Imprime el tiempo de entrenamiento.
    """

    # Se obtiene la ruta del archivo a través de XCom.
    file_path = context['ti'].xcom_pull(task_ids = 'load_data', key = 'file_path')

    # Se leen los datos formato parquet.
    df = pd.read_parquet(file_path)

    # Se configuran los datos.
    X = df[PARAM_COLS + ["key", "mode", "genre"]]
    y = df["valence"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Se entrena el modelo.
    pipeline = build_pipeline(n_jobs = -1)

    t0 = time.perf_counter()
    pipeline.fit(X_train, y_train)
    training_time = time.perf_counter() - t0

    print(f"Tiempo total de entrenamiento: {training_time:.2f} [s].")



# ── Definición del DAG ────────────────────────────────────────────────────────

with DAG(
    dag_id="spotify_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["mds7202", "spotify"],
) as dag:
    load_data = PythonOperator(
        task_id="load_data",
        python_callable=task_load_data_fn,
    )

    train_model = PythonOperator(
        task_id="train_model",
        python_callable=task_train_model_fn,
    )

    # TODO: define la dependencia entre tareas (load_data debe ejecutarse antes que train_model)
    load_data >> train_model
