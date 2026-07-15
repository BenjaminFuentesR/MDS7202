# app.py


# Librerías.
import os

import gradio as gr
from services import enviar_prediccion

# Configuración.
tema_chaucher = gr.themes.Soft(primary_hue="blue", secondary_hue="indigo", neutral_hue="slate")

# Main: Se define la interfaz usando blocks.
with gr.Blocks(title="ChaucherApp - Soporte") as app:
    # Encabezado.
    gr.Markdown(
        """
        <h1 style='text-align: center; color: #1E3A8A;'> ChaucherApp Soporte</h1>
        <h3 style='text-align: center;'>Clasificador de Prioridad de Tickets</h3>
        """
    )

    with gr.Row():
        # Sección 1: Atributos del Usuario.
        with gr.Column(variant="panel"):
            gr.Markdown("### Atributos del Usuario")

            canal_input = gr.Dropdown(
                choices=["Whatsapp", "Web", "Página Web", "Correo"],
                label="Canal",
                value="Whatsapp",
                info="Canal por el cual el usuario nos contactó.",
            )

            categoria_input = gr.Dropdown(
                choices=["Cuenta", "Fraude", "Cobros", "Técnica", "Pregunta general", "Otro"],
                label="Categoría",
                value="Pregunta general",
                info="Categoría general asignada por el sistema.",
            )

        # Sección 2: Atributos del Ticket.
        with gr.Column(variant="panel"):
            gr.Markdown("### Atributos del Ticket")

            asunto_input = gr.Textbox(label="Asunto", placeholder="Ejemplo: Transferencia no recibida y...", lines=1)

            contenido_input = gr.Textbox(
                label="Contenido", placeholder="Mensaje exacto enviado por el cliente...", lines=5
            )

    # Se crea boton para resultado.
    with gr.Row():
        btn_predecir = gr.Button("Clasificar Prioridad", variant="primary", size="lg")

    with gr.Row():
        output = gr.Textbox(label="Resultado de la Evaluación", interactive=False, lines=2)

    # Conexión del botón con la función de backend.
    btn_predecir.click(
        fn=enviar_prediccion, inputs=[asunto_input, contenido_input, canal_input, categoria_input], outputs=output
    )


if __name__ == "__main__":
    host = "0.0.0.0" if os.getenv("IS_DOCKER") else "127.0.0.1"
    app.launch(server_name=host, server_port=7860, share=False, theme=tema_chaucher)
