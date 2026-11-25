"""Ejemplo 4: cuánta memoria ocupa el modelo cargado según la ventana de contexto.

    python sesion_03_llm_tokens_contexto/ejemplos/04_memoria_del_modelo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm, ollama  # noqa: E402

for contexto in (2048, 8192, 32768):
    ollama.chat_nativo("Hola", opciones={"num_ctx": contexto, "num_predict": 1})
    for m in ollama.modelos_cargados():
        if m["name"].startswith(llm.MODELO_CHAT.split(":")[0]):
            print(f"num_ctx={contexto:6}: {m['size'] / 1024**3:.2f} GB en memoria "
                  f"({m.get('size_vram', 0) / 1024**3:.2f} GB en GPU)")
