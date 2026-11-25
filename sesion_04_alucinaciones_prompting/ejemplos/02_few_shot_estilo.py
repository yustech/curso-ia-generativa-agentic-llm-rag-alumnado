"""Ejemplo 2: few-shot para imponer un estilo propio (historias de usuario de Atlántica).

    python sesion_04_alucinaciones_prompting/ejemplos/02_few_shot_estilo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

PETICION = "Las tiendas quieren descargar el albarán firmado de cada entrega."

print("Zero-shot:\n", llm.chat(f"Convierte en historia de usuario: {PETICION}", temperatura=0), "\n")

mensajes = [
    {"role": "system", "content": "Conviertes peticiones en historias de usuario con el formato de Atlántica."},
    {"role": "user", "content": "Las tiendas quieren ver dónde está el camión."},
    {"role": "assistant", "content": (
        "Como tienda quiero ver en un mapa la posición del camión para saber cuándo llega mi pedido.\n"
        "- Dado un envío en ruta, cuando abro su detalle, entonces veo la posición actualizada hace menos de 2 minutos.\n"
        "- Dado un envío entregado, cuando abro su detalle, entonces no se muestra el mapa.\n"
        "Estimación: 8 puntos")},
    {"role": "user", "content": PETICION},
]
print("Few-shot:\n", llm.chat(mensajes, temperatura=0))
