"""Ejemplo 3: el efecto de la temperatura.

    python sesion_03_llm_tokens_contexto/ejemplos/03_temperatura.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

PROMPT = "Propón un nombre corto para un asistente de IA de una empresa logística. Responde solo con el nombre."

for temperatura in (0.0, 0.7, 1.5):
    nombres = [llm.chat(PROMPT, temperatura=temperatura, max_tokens=15) for _ in range(5)]
    print(f"temperatura {temperatura}: {nombres}")
