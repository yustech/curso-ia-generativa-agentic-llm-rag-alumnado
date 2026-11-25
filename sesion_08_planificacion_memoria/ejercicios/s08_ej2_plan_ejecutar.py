"""Sesión 8 - Ejercicio 2: patrón planificar-ejecutar.

El modelo propone un plan completo (JSON validado), el programa lo valida y lo
ejecuta paso a paso, y el modelo redacta la respuesta final con los resultados.
El plan se puede revisar (o aprobar) antes de ejecutarlo.

    python sesion_08_planificacion_memoria/ejercicios/s08_ej2_plan_ejecutar.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402
from comun.herramientas import ejecutar_herramienta  # noqa: E402


class Paso(BaseModel):
    numero: int
    descripcion: str
    herramienta: str | None = Field(default=None, description="Nombre de la herramienta, o null si el paso no necesita ninguna")
    argumentos: dict[str, Any] = Field(default_factory=dict)


class Plan(BaseModel):
    objetivo: str
    pasos: list[Paso]


def planificar(objetivo: str, descripcion_herramientas: str, max_pasos: int = 5) -> Plan:
    """Pide al modelo un plan con ``llm.estructurado``. El mensaje de sistema explica las herramientas
    disponibles (``descripcion_herramientas``) y el máximo de pasos."""
    raise NotImplementedError("Completa este bloque")


def validar_plan(plan: Plan, herramientas: set[str], max_pasos: int = 5) -> list[str]:
    """Problemas del plan: «El plan no tiene pasos», «El plan tiene N pasos (máximo M)»,
    «Paso N: herramienta desconocida X» y «Los pasos no están numerados de 1 a N»."""
    raise NotImplementedError("Completa este bloque")


def ejecutar_plan(plan: Plan, registro: dict[str, Callable[..., Any]], detener_en_error: bool = True) -> list[dict]:
    """Ejecuta los pasos en orden. Cada resultado es ``{"numero", "descripcion", "estado", "resultado"}``
    con estado «ok», «error» (si el resultado empieza por «ERROR:») o «sin_herramienta».
    Si ``detener_en_error`` y un paso falla, los siguientes se marcan como «omitido» con resultado vacío."""
    raise NotImplementedError("Completa este bloque")


def sintetizar(objetivo: str, resultados: list[dict]) -> str:
    """Pide al modelo la respuesta final a partir del objetivo y de los resultados de cada paso
    (uno por línea: «Paso N (estado): resultado»). Si algún paso falló, debe decirlo."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    from comun.herramientas import buscar_documentacion, calcular

    registro = {"buscar_documentacion": buscar_documentacion, "calcular": calcular}
    descripcion = ("- buscar_documentacion(consulta: str): busca en la documentación de Atlántica.\n"
                   "- calcular(expresion: str): calcula una expresión aritmética.")
    objetivo = "Calcula el coste mensual de dos máquinas m6i.large y una base de datos db.t3.medium según el catálogo."
    plan = planificar(objetivo, descripcion)
    print(plan.model_dump_json(indent=2))
    problemas = validar_plan(plan, set(registro))
    if problemas:
        print("Plan no válido:", problemas)
    else:
        resultados = ejecutar_plan(plan, registro)
        print(sintetizar(objetivo, resultados))
