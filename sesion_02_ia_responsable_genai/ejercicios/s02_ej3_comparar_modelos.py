"""Sesión 2 - Ejercicio 3: comparar modelos con la misma pregunta.

Ejecuta con el modelo real (tarda unos minutos):
    python sesion_02_ia_responsable_genai/ejercicios/s02_ej3_comparar_modelos.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

MODELOS = ["granite4:micro", "gemma3:4b", "qwen3:4b"]
PREGUNTAS = [
    "Resume en una frase qué es la gestión de cambios en TI.",
    "¿Cuánto es 17 × 23? Responde solo con el número.",
    "Escribe una función Python que devuelva True si un número es primo.",
]


def ejecutar_en_modelo(pregunta: str, modelo: str) -> dict:
    """Llama al modelo y devuelve un diccionario con:
    ``modelo``, ``respuesta``, ``segundos``, ``tokens_salida`` y ``tokens_por_segundo`` (redondeado a 1 decimal).

    Usa ``llm.chat(..., modelo=modelo, temperatura=0)`` y lee las métricas de ``llm.ultima_llamada``.
    """
    raise NotImplementedError("Completa este bloque")


def comparar_modelos(pregunta: str, modelos: list[str]) -> list[dict]:
    """Ejecuta la pregunta en cada modelo. Si un modelo falla, su ``respuesta`` empieza por ``ERROR:``
    y los números valen 0 (la comparación continúa con los demás)."""
    raise NotImplementedError("Completa este bloque")


def tabla_markdown(resultados: list[dict], ancho: int = 60) -> str:
    """Tabla: | Modelo | Segundos | Tokens | Tokens/s | Respuesta |
    Segundos con 1 decimal. La respuesta se recorta a ``ancho`` caracteres, sin saltos de línea
    (sustituidos por espacios) y añadiendo «…» si se ha recortado."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    disponibles = llm.modelos_disponibles()
    modelos = [m for m in MODELOS if any(d.startswith(m) for d in disponibles)]
    for pregunta in PREGUNTAS:
        print(f"\n### {pregunta}\n")
        print(tabla_markdown(comparar_modelos(pregunta, modelos)))
