"""Ejemplo 2: tokens contados por el propio modelo (Ollama) frente a tiktoken.

    python sesion_03_llm_tokens_contexto/ejemplos/02_tokens_del_modelo.py
"""

import sys
from pathlib import Path

import tiktoken

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import ollama  # noqa: E402

codificador = tiktoken.get_encoding("o200k_base")
texto = (Path(__file__).resolve().parents[2] / "datos" / "atlantica" / "documentos"
         / "11_politica_vacaciones_teletrabajo.md").read_text(encoding="utf-8")

base = ollama.chat_nativo("Hola", opciones={"num_ctx": 4096, "num_predict": 1})["prompt_eval_count"]
for modelo in ["granite4:micro", "gemma3:4b", "qwen3:4b"]:
    try:
        r = ollama.chat_nativo(texto, modelo=modelo, opciones={"num_ctx": 4096, "num_predict": 1})
        print(f"{modelo:16} {r['prompt_eval_count']:5} tokens (incluye la plantilla de chat)")
    except Exception as error:
        print(f"{modelo:16} no disponible ({type(error).__name__})")
print(f"{'tiktoken':16} {len(codificador.encode(texto)):5} tokens")
print(f"\nLa plantilla de chat de granite4:micro añade unos {base - len(codificador.encode('Hola'))} tokens fijos.")
