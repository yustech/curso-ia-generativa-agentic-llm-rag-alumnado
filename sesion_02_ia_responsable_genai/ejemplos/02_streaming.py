"""Ejemplo 2: respuesta en streaming (token a token), como en las interfaces de chat.

    python sesion_02_ia_responsable_genai/ejemplos/02_streaming.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

inicio = time.perf_counter()
primer_token = None
flujo = llm.cliente().chat.completions.create(
    model=llm.MODELO_CHAT,
    messages=[{"role": "user", "content": "Describe en 5 líneas cómo funciona un almacén logístico."}],
    stream=True,
)
for trozo in flujo:
    texto = (trozo.choices[0].delta.content or "") if trozo.choices else ""
    if texto and primer_token is None:
        primer_token = time.perf_counter() - inicio
    print(texto, end="", flush=True)

print(f"\n\nTiempo hasta el primer token: {primer_token:.2f} s · total: {time.perf_counter() - inicio:.2f} s")
print("El streaming no acelera la respuesta: mejora la percepción de velocidad.")
