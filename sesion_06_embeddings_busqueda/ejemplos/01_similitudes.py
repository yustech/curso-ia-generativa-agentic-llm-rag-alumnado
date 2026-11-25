"""Ejemplo 1: el significado como geometría. Matriz de similitudes entre frases.

    python sesion_06_embeddings_busqueda/ejemplos/01_similitudes.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

FRASES = [
    "¿Con cuánta antelación pido las vacaciones?",
    "Las vacaciones se solicitan con 15 días naturales de antelación.",
    "El Comité de Cambios se reúne los jueves.",
    "¿Cuándo es la reunión del CAB?",
    "When is the change advisory board meeting?",
    "El camión frigorífico llegó tarde a la tienda.",
]

v = np.array(llm.embeddings(FRASES))
v /= np.linalg.norm(v, axis=1, keepdims=True)
similitudes = v @ v.T

print("      " + "  ".join(f"F{i}" for i in range(len(FRASES))))
for i, fila in enumerate(similitudes):
    print(f"F{i}  " + "  ".join(f"{x:.2f}"[1:] if x < 1 else "1.0" for x in fila) + f"   {FRASES[i][:45]}")
print("\nObserva: F3 (CAB) y F2 (Comité de Cambios) se parecen sin compartir palabras; F4 está en inglés y también.")
