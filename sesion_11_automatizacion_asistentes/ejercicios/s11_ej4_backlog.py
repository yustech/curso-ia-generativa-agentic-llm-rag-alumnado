"""Sesión 11 - Ejercicio 4: priorizar el backlog del asistente y planificar sprints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ORDEN_MOSCOW = {"M": 0, "S": 1, "C": 2, "W": 3}  # Must, Should, Could, Won't


@dataclass
class Historia:
    id: str
    titulo: str
    valor: int        # 1 a 10
    esfuerzo: int     # puntos: 1, 2, 3, 5, 8, 13
    moscow: Literal["M", "S", "C", "W"]


def puntuacion(h: Historia) -> float:
    """Valor / esfuerzo con 2 decimales."""
    raise NotImplementedError("Completa este bloque")


def priorizar(historias: list[Historia]) -> list[Historia]:
    """Orden: MoSCoW (M, S, C, W), después mayor puntuación y, a igualdad, id ascendente."""
    raise NotImplementedError("Completa este bloque")


def planificar_sprints(historias: list[Historia], capacidad: int, max_sprints: int = 3) -> list[list[str]]:
    """Reparte las historias priorizadas (sin las «W») en sprints de ``capacidad`` puntos.

    Recorre las historias en orden de prioridad; cada una va al primer sprint con hueco
    (creando uno nuevo si hace falta, hasta ``max_sprints``). Una historia más grande que la
    capacidad o que no cabe en ningún sprint se queda fuera. Devuelve listas de ids.
    """
    raise NotImplementedError("Completa este bloque")


def a_markdown(historias: list[Historia]) -> str:
    """Tabla priorizada: | Prioridad | Id | Historia | MoSCoW | Valor | Esfuerzo | Valor/esfuerzo |"""
    raise NotImplementedError("Completa este bloque")
