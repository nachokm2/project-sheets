from openai import OpenAI
import json
import requests

client = OpenAI()

def buscar_estudiante(identificador, tipo):
    response = requests.post("https://project-sheets.onrender.com/api/matricula", json={
        "identificador": identificador,
        "tipo": tipo
    })
    return response.json()

# Crear un hilo
thread = client.beta.threads.create()

# Agregar mensaje del usuario
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

                # Enviar resultado al asistente
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

# Mostrar respuesta final
mensajes = client.beta.threads.messages.list(thread_id=thread.id)
for msg in mensajes.data:
    print(msg.role, ":", msg.content[0].text.value)
