"""Índice RAG del equipo (versión de partida).

Parte del buscador semántico de referencia del curso. En las sesiones 6 y 7
lo sustituiréis por vuestra versión: búsqueda híbrida, ingesta incremental en
Chroma y la estrategia de troceado que mejor puntúe con
``evals/preguntas_recuperacion.jsonl``.
"""

from __future__ import annotations

import os
from pathlib import Path

import entorno  # noqa: F401  (configura sys.path)
from comun import llm
from comun.buscador import BuscadorSemantico, contexto_numerado
from comun.documentos import CARPETA_DOCUMENTOS

CARPETA_FUENTES = Path(os.getenv("CARPETA_FUENTES", CARPETA_DOCUMENTOS))
_BUSCADORES: dict[bool, BuscadorSemantico] = {}


def buscador() -> BuscadorSemantico:
    modo = llm.es_falso()
    if modo not in _BUSCADORES:
        _BUSCADORES[modo] = BuscadorSemantico.de_documentos(CARPETA_FUENTES)
    return _BUSCADORES[modo]


def buscar(consulta: str, k: int = 3) -> list[dict]:
    """Resultados como diccionarios (para la interfaz y la evaluación)."""
    return [{"fuente": t.documento, "seccion": t.seccion, "referencia": t.referencia, "puntuacion": p, "texto": t.texto}
            for t, p in buscador().buscar(consulta, k)]


def contexto(consulta: str, k: int = 3) -> str:
    """Bloques numerados ``[n] documento › sección`` para el prompt."""
    return contexto_numerado(buscador().buscar(consulta, k))
