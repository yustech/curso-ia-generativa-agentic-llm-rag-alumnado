"""Sesión 7 - Ejercicio 2: evaluar el RAG de extremo a extremo y checklist de calidad.

Se miden por separado la recuperación (¿se recupera la fuente correcta?) y la
generación (¿se abstiene cuando debe?, ¿cita la fuente correcta?, ¿responde lo esperado?).

    python sesion_07_indexacion_agentes/ejercicios/s07_ej2_evaluar_rag.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import DATOS, llm  # noqa: E402

RUTA_PREGUNTAS = DATOS / "evaluacion" / "preguntas_rag.jsonl"
NO_CONSTA = "no consta"

UMBRALES = {"recuperacion_hit": 0.85, "abstencion_correcta": 1.0, "cita_correcta": 0.80, "cobertura_respuesta": 0.50}


@dataclass
class Resultado:
    """Lo que devuelve el sistema RAG que se evalúa."""

    texto: str
    documentos: list[str]  # documento de cada fragmento recuperado, en orden ([1], [2], ...)


def _normal(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def se_abstiene(texto: str) -> bool:
    """True si la respuesta contiene «no consta» (sin distinguir mayúsculas ni tildes)."""
    raise NotImplementedError("Completa este bloque")


def documentos_citados(texto: str, documentos: list[str]) -> set[str]:
    """Documentos de los fragmentos citados con [n] (n desde 1). Se ignoran números fuera de rango."""
    raise NotImplementedError("Completa este bloque")


def cobertura(respuesta: str, esperado: str) -> float:
    """Proporción de términos de más de 3 caracteres del texto esperado (normalizados, sin
    puntuación en los extremos) que aparecen en la respuesta normalizada. 1.0 si no hay términos."""
    raise NotImplementedError("Completa este bloque")


def evaluar_pregunta(pregunta: dict, resultado: Resultado) -> dict:
    """Métricas de una pregunta.

    Con fuente: ``recuperacion_hit`` (la fuente está entre los documentos recuperados),
    ``cita_correcta`` (la fuente está entre los citados), ``cobertura_respuesta``.
    Sin fuente (``fuente`` null): ``abstencion_correcta`` (se abstiene).
    Siempre incluye ``"id"``.
    """
    raise NotImplementedError("Completa este bloque")


def agregar(por_pregunta: list[dict]) -> dict[str, float]:
    """Media (3 decimales) de cada métrica sobre las preguntas en las que aparece. True cuenta 1."""
    raise NotImplementedError("Completa este bloque")


def checklist(metricas: dict[str, float], umbrales: dict[str, float] = UMBRALES) -> list[dict]:
    """Una fila por umbral: ``{"criterio", "valor", "umbral", "cumple"}``. Si falta la métrica, valor None y no cumple."""
    raise NotImplementedError("Completa este bloque")


def evaluar(responder: Callable[[str], Resultado], preguntas: list[dict]) -> tuple[list[dict], dict[str, float]]:
    """Ejecuta el sistema con todas las preguntas y devuelve ``(por_pregunta, agregado)``."""
    por_pregunta = [evaluar_pregunta(p, responder(p["pregunta"])) for p in preguntas]
    return por_pregunta, agregar(por_pregunta)


def rag_de_referencia(k: int = 4) -> Callable[[str], Resultado]:
    """Sistema RAG que se evalúa: buscador de referencia + prompt con citas."""
    from comun.buscador import BuscadorSemantico, contexto_numerado

    buscador = BuscadorSemantico.de_documentos()
    sistema = ("Responde SOLO con la información de los fragmentos y cita cada dato con [n]. "
               "Si la respuesta no está en los fragmentos, responde «No consta en la documentación».")

    def responder(pregunta: str) -> Resultado:
        resultados = buscador.buscar(pregunta, k)
        texto = llm.chat(f"{contexto_numerado(resultados)}\n\nPregunta: {pregunta}", sistema=sistema, temperatura=0)
        return Resultado(texto, [t.documento for t, _ in resultados])

    return responder


if __name__ == "__main__":
    with RUTA_PREGUNTAS.open(encoding="utf-8") as f:
        preguntas = [json.loads(l) for l in f if l.strip()]
    por_pregunta, agregado = evaluar(rag_de_referencia(), preguntas)
    for fila in checklist(agregado):
        print(f"{'OK ' if fila['cumple'] else 'NO '} {fila['criterio']:22} {fila['valor']} (umbral {fila['umbral']})")
    print("\nPreguntas con problemas:")
    for fila in por_pregunta:
        if not all(v for k, v in fila.items() if k != "id" and isinstance(v, bool)):
            print(fila)
