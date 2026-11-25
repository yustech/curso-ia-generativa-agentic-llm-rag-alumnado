"""Sesión 6 - Ejercicio 3: métricas de recuperación y tabla comparativa.

    python sesion_06_embeddings_busqueda/ejercicios/s06_ej3_metricas.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

RUTA_PREGUNTAS = Path(__file__).resolve().parents[2] / "datos" / "atlantica" / "evaluacion" / "preguntas_rag.jsonl"


def acierto_en_k(documentos: list[str], relevante: str, k: int) -> bool:
    """True si ``relevante`` está entre los ``k`` primeros documentos."""
    raise NotImplementedError("Completa este bloque")


def rango_reciproco(documentos: list[str], relevante: str) -> float:
    """1 / posición de la primera aparición de ``relevante`` (posiciones desde 1). 0.0 si no aparece."""
    raise NotImplementedError("Completa este bloque")


def cargar_preguntas(ruta: Path = RUTA_PREGUNTAS) -> list[dict]:
    """Preguntas del JSONL que tienen ``fuente`` (se descartan las de fuente null)."""
    raise NotImplementedError("Completa este bloque")


def evaluar(buscar: Callable[[str, int], list], preguntas: list[dict], k: int = 5) -> dict:
    """Evalúa un buscador. ``buscar(pregunta, k)`` devuelve ``[(trozo, puntuación), ...]`` y cada
    trozo tiene ``.documento``. La fuente relevante de cada pregunta es ``pregunta["fuente"]``.

    Devuelve ``{"hit@k": proporción con 3 decimales, "mrr": media con 3 decimales,
    "fallos": [ids de las preguntas sin acierto en k]}``.
    """
    raise NotImplementedError("Completa este bloque")


def tabla(resultados: dict[str, dict], k: int) -> str:
    """Tabla Markdown ``| Estrategia | Hit@<k> | MRR | Fallos |`` en el orden del diccionario.
    Hit y MRR con 3 decimales; los fallos separados por comas o «—» si no hay."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    from comun.documentos import cargar_trozos
    from s06_ej2_busqueda import BuscadorBM25, BuscadorHibrido, BuscadorSemantico

    trozos = cargar_trozos()
    bm25, semantico = BuscadorBM25(trozos), BuscadorSemantico(trozos)
    estrategias = {"BM25": bm25, "Semántica": semantico, "Híbrida (RRF)": BuscadorHibrido(bm25, semantico)}
    preguntas = cargar_preguntas()
    for k in (1, 3):
        print(f"\n{tabla({n: evaluar(b.buscar, preguntas, k) for n, b in estrategias.items()}, k)}")
