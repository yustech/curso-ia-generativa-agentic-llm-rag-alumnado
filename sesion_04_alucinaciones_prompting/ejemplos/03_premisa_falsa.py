"""Ejemplo 3: complacencia ante una premisa falsa y cómo corregirla con el prompt.

    python sesion_04_alucinaciones_prompting/ejemplos/03_premisa_falsa.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

PREGUNTA = "¿Por qué la política de Atlántica permite buckets públicos en producción?"
POLITICA = "Política de Atlántica: todos los buckets son privados y cifrados. Está prohibido cualquier bucket con acceso público."

print("Sin instrucciones:\n", llm.chat(f"{POLITICA}\n\n{PREGUNTA}", temperatura=0), "\n")
print("Con instrucción de verificar la premisa:\n", llm.chat(
    f"{POLITICA}\n\n{PREGUNTA}", temperatura=0,
    sistema="Antes de responder, comprueba si la pregunta parte de una premisa falsa según el texto. Si es así, corrígela."))
