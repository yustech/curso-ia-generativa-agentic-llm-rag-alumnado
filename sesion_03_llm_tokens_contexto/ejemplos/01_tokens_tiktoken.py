"""Ejemplo 1: ver los tokens de distintos textos.

    python sesion_03_llm_tokens_contexto/ejemplos/01_tokens_tiktoken.py
"""

import tiktoken

codificador = tiktoken.get_encoding("o200k_base")

TEXTOS = {
    "español": "La logística inversa recupera los palés vacíos de las tiendas.",
    "inglés": "Reverse logistics recovers empty pallets from the stores.",
    "número": "El pedido 48.379 pesa 1.234,56 kg.",
    "código": "def precio_con_iva(base: Decimal) -> Decimal:",
    "rara": "Ferrocarrilero electroencefalografista",
}

for nombre, texto in TEXTOS.items():
    ids = codificador.encode(texto)
    trozos = [codificador.decode([i]) for i in ids]
    print(f"{nombre:8} {len(texto.split()):2} palabras · {len(ids):2} tokens · {trozos}")
