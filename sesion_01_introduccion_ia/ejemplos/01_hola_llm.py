"""Ejemplo 1: tu primera llamada a un LLM local.

Ejecuta desde la raíz del repositorio:
    python sesion_01_introduccion_ia/ejemplos/01_hola_llm.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from comun import llm  # noqa: E402

print(llm.describir_configuracion())
print()

respuesta = llm.chat(
    "Explica en dos frases qué es un operador logístico.",
    sistema="Eres un asistente que responde en español, de forma breve y precisa.",
)
print(respuesta)
print()
m = llm.ultima_llamada
print(f"Modelo: {m.modelo} · {m.segundos:.1f} s · {m.tokens_entrada} tokens de entrada · "
      f"{m.tokens_salida} de salida · {m.tokens_por_segundo:.1f} tokens/s")
