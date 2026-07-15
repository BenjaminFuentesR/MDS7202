# generate_prediction.py


# Librerías.
import cloudpickle
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Preparación.

ROOT_PATH = ""

# Se cargan variables de entorno.
load_dotenv(f"{ROOT_PATH}.env")

# Se carga el pipeline del modelo entrenado.
MODEL_PATH = f"{ROOT_PATH}modelo_final.pkl"
with open(MODEL_PATH, "rb") as f:
    pipeline_modelo = cloudpickle.load(f)

# Se inicializa el cliente de Embeddings de Gemini.
embeddings_client = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", output_dimensionality=1024)


# Main.
def generate_prediction(asunto: str, contenido: str, canal: str, categoria: str) -> str:
    """
    Recibe los campos de un ticket, construye el vector de embeddings con Gemini,
    estructura los datos según lo que espera el pipeline y retorna la predicción.
    """

    # Se vectoriza como gemini.
    text_to_embedding = f"Asunto_Ticket: {asunto}\nContenido_Ticket: {contenido}\n"
    vector_embedding = embeddings_client.embed_query(text_to_embedding)

    # Se estructuran los datos según lo que espera el pipeline.
    combined_text = f"{asunto} {contenido}".strip()
    n_chars = len(combined_text)

    data_dict = {
        "N_Caracteres_Ticket": [n_chars],
        "Canal_Ticket": [canal],
        "Categoría_Problema": [categoria],
        "Texto": [combined_text],
    }

    # Se agregan los embeddings.
    for i, valor in enumerate(vector_embedding):
        data_dict[f"embedding_dim_{i + 1}"] = [valor]

    df_input = pd.DataFrame(data_dict)

    # Se hace la predicción.
    predictions = pipeline_modelo.predict(df_input)

    return str(predictions[0])


# terminal.
if __name__ == "__main__":
    print("-" * 50)
    print("Prueba predicción de ticket")
    print("-" * 50)
    print("\n")

    # Se carga el dataset original.
    df_tickets = pd.read_parquet(f"{ROOT_PATH}data/tickets.parquet")

    # Se selecciona un ticket al azar.
    sample_ticket = df_tickets.sample(1, random_state=42).iloc[0]

    # Se extraen los campos necesarios.
    test_asunto = sample_ticket["Asunto_Ticket"]
    test_contenido = sample_ticket["Contenido_Ticket"]
    test_canal = sample_ticket["Canal_Ticket"]
    test_categoria = sample_ticket["Categoría_Problema"]
    prioridad_real = sample_ticket["Nivel_Prioridad"]

    print("-" * 50)
    print(f"Datos del ticket ID: {sample_ticket['Id_Ticket']}")
    print(f"Asunto   : {test_asunto}")
    print(f"Canal    : {test_canal}")
    print(f"Categoría: {test_categoria}")
    print("-" * 50)

    # Se hace la predicción.
    result = generate_prediction(
        asunto=test_asunto, contenido=test_contenido, canal=test_canal, categoria=test_categoria
    )

    print(f"Predicción del modelo: {result}")
    print(f"Prioridad real: {prioridad_real}")
    print("-" * 50)
