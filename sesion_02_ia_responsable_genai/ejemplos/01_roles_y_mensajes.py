"""Ejemplo 1: el mensaje de sistema cambia el comportamiento; el modelo no recuerda nada.

    python sesion_02_ia_responsable_genai/ejemplos/01_roles_y_mensajes.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

PREGUNTA = "¿Puedo pegar el contrato de un cliente en un chatbot de internet para que me lo resuma?"

print("1) Sin mensaje de sistema:\n", llm.chat(PREGUNTA), "\n")

SISTEMA = (
    "Eres el asistente interno de Atlántica Logística. Respondes en español, en menos de 60 palabras. "
    "Regla de la empresa: está prohibido introducir información Confidencial (como contratos de clientes) "
    "en herramientas de IA externas no aprobadas; la herramienta aprobada es Faro-IA."
)
print("2) Con mensaje de sistema:\n", llm.chat(PREGUNTA, sistema=SISTEMA), "\n")

print("3) Sin memoria: primero me presento, después pregunto por mi nombre en otra llamada")
llm.chat("Me llamo Lucía y soy jefa de proyecto.")
print("   ", llm.chat("¿Cómo me llamo?"))

print("\n4) Con memoria: reenvío el historial")
historial = [{"role": "user", "content": "Me llamo Lucía y soy jefa de proyecto."}]
historial.append({"role": "assistant", "content": llm.chat(historial)})
historial.append({"role": "user", "content": "¿Cómo me llamo?"})
print("   ", llm.chat(historial))
