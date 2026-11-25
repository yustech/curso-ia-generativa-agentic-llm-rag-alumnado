"""Sesión 11 - Ejercicio 1: modelar un proceso AS-IS / TO-BE y medir la automatización.

    python sesion_11_automatizacion_asistentes/ejercicios/s11_ej1_proceso.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Tipo = Literal["manual", "automatico", "ia"]


@dataclass
class Paso:
    nombre: str
    actor: str
    tipo: Tipo
    minutos: float
    control_humano: bool = False  # la persona revisa o aprueba en este paso


@dataclass
class Proceso:
    nombre: str
    pasos: list[Paso] = field(default_factory=list)


def tiempo_total(proceso: Proceso) -> float:
    """Suma de los minutos de todos los pasos."""
    raise NotImplementedError("Completa este bloque")


def porcentaje_automatizado(proceso: Proceso) -> float:
    """Porcentaje del tiempo en pasos «automatico» o «ia» (1 decimal). 0.0 si el proceso no tiene tiempo."""
    raise NotImplementedError("Completa este bloque")


def avisos(proceso: Proceso) -> list[str]:
    """Avisos de diseño del TO-BE:

    - «<paso>: paso de IA sin control humano posterior» si un paso «ia» no tiene después (o en él mismo)
      ningún paso con ``control_humano``.
    - «<paso>: control humano sin actor humano» si un paso con control humano tiene tipo distinto de «manual».
    """
    raise NotImplementedError("Completa este bloque")


def comparar(as_is: Proceso, to_be: Proceso) -> dict:
    """``{"antes": min, "despues": min, "ahorro_minutos", "ahorro_porcentaje" (1 decimal),
    "pasos_ia": n en el TO-BE, "controles_humanos": n en el TO-BE}``."""
    raise NotImplementedError("Completa este bloque")


def a_mermaid(proceso: Proceso) -> str:
    """Diagrama ``flowchart LR`` con un nodo por paso (ids P1, P2…) unidos en orden.

    Forma según el tipo: manual ``P1["texto"]``, automatico ``P1[["texto"]]``, ia ``P1(["texto"])``.
    El texto es «nombre · actor · N min» y, si hay control humano, se añade « ✋».
    """
    raise NotImplementedError("Completa este bloque")


AS_IS = Proceso("Informe de estado semanal (AS-IS)", [
    Paso("Leer actas de la semana", "Jefa de proyecto", "manual", 40),
    Paso("Consultar backlog y calcular avance", "Jefa de proyecto", "manual", 30),
    Paso("Actualizar matriz de riesgos", "Jefa de proyecto", "manual", 20),
    Paso("Redactar informe", "Jefa de proyecto", "manual", 45),
    Paso("Revisar y enviar", "Jefa de proyecto", "manual", 10, control_humano=True),
])
TO_BE = Proceso("Informe de estado semanal (TO-BE)", [
    Paso("Extraer acciones y riesgos de las actas", "PMO Copilot", "ia", 2),
    Paso("Calcular avance del sprint", "Backlog", "automatico", 1),
    Paso("Redactar borrador con fuentes", "PMO Copilot", "ia", 2),
    Paso("Revisar, corregir y aprobar", "Jefa de proyecto", "manual", 20, control_humano=True),
    Paso("Enviar a dirección", "Correo", "automatico", 1),
])

if __name__ == "__main__":
    print(comparar(AS_IS, TO_BE))
    print("Avisos TO-BE:", avisos(TO_BE) or "ninguno")
    print(a_mermaid(TO_BE))
