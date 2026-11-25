"""Sesión 10 - Ejercicio 3: flujo multiagente con LangGraph (investigador, redactor y revisor).

    investigador ──► redactor ──► revisor ──┬─► FIN (aprobado o máximo de revisiones)
                        ▲                   │
                        └───── correcciones ┘

    python sesion_10_multiagente_frameworks/ejercicios/s10_ej3_multiagente.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, TypedDict

from langgraph.graph import END, START, StateGraph

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

MAX_REVISIONES = 2


class Estado(TypedDict, total=False):
    pregunta: str
    notas: str
    borrador: str
    revision: str
    aprobado: bool
    iteraciones: int


def nodo_investigador(estado: Estado, buscar: Callable[[str], str]) -> dict:
    """Busca con ``buscar(pregunta)`` y pide al LLM unas notas con los datos relevantes y su fuente.
    Devuelve ``{"notas": ..., "iteraciones": 0}``."""
    raise NotImplementedError("Completa este bloque")


def nodo_redactor(estado: Estado) -> dict:
    """Redacta la respuesta a partir de las notas. Si hay una revisión anterior no aprobada, la incluye
    en el prompt como «Correcciones del revisor: …». Devuelve ``{"borrador": ...}``."""
    raise NotImplementedError("Completa este bloque")


def nodo_revisor(estado: Estado) -> dict:
    """Compara el borrador con las notas. El LLM debe responder «APROBADO» o una lista de correcciones.
    Devuelve ``{"revision": texto, "aprobado": texto empieza por APROBADO (sin distinguir mayúsculas),
    "iteraciones": iteraciones + 1}``."""
    raise NotImplementedError("Completa este bloque")


def siguiente(estado: Estado) -> str:
    """Arista condicional tras el revisor: ``END`` si está aprobado o si ``iteraciones >= MAX_REVISIONES``;
    si no, ``"redactor"``."""
    raise NotImplementedError("Completa este bloque")


def construir_grafo(buscar: Callable[[str], str]):
    """Grafo: START → investigador → redactor → revisor → (siguiente). Devuelve el grafo compilado."""
    raise NotImplementedError("Completa este bloque")


def ejecutar(pregunta: str, buscar: Callable[[str], str]) -> Estado:
    return construir_grafo(buscar).invoke({"pregunta": pregunta})


if __name__ == "__main__":
    from comun.herramientas import buscar_documentacion

    final = ejecutar("¿Qué tiene que incluir una solicitud de cambio normal y cuándo se presenta?", buscar_documentacion)
    print("NOTAS:\n", final["notas"], "\n\nRESPUESTA:\n", final["borrador"])
    print(f"\nRevisiones: {final['iteraciones']} · aprobado: {final['aprobado']}")
