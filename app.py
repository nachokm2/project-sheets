from openai import OpenAI
import json
import requests
import time

client = OpenAI()

def buscar_estudiante(identificador, tipo):
    url = "https://project-sheets.onrender.com/api/matricula"
    payload = {
        "identificador": identificador,
        "tipo": tipo
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al consultar la API: {str(e)}"}

def main():
    # Crear un hilo nuevo
    thread = client.beta.threads.create()

    # Enviar mensaje inicial
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="¿Cuál es el estado de matrícula del estudiante con RUT 12345678-9?"
    )

    # Ejecutar el asistente
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_eh2jnFxcgzhVif20Nnt0PmUh"
    )

    # Esperar respuesta
    while True:
        run_info = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run_info.status == "completed":
            break

        if run_info.status == "requires_action":
            for call in run_info.required_action.submit_tool_outputs.tool_calls:
                if call.function.name == "buscar_estudiante":
                    args = json.loads(call.function.arguments)
                    resultado = buscar_estudiante(args["identificador"], args["tipo"])

                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=[
                            {
                                "tool_call_id": call.id,
                                "output": json.dumps(resultado)
                            }
                        ]
                    )
        time.sleep(1)  # Para no saturar el loop

    # Mostrar respuesta final
    mensajes = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in mensajes.data:
        # Mensajes pueden tener distintas estructuras, tratar de imprimir seguro
        content = msg.content
        if isinstance(content, list) and len(content) > 0:
            # Por lo general es lista con diccionario que tiene 'text' o 'value'
            texto = content[0].get('text') or content[0].get('value') or str(content[0])
            print(f"{msg.role}: {texto}")
        else:
            print(f"{msg.role}: {content}")

if __name__ == "__main__":
    main()
