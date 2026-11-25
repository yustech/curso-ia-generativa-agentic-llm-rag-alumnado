"""Sesión 13 - Ejercicio 1: evaluación de extremo a extremo con conjunto dorado, juez y línea base.

    python sesion_13_casos_produccion/ejercicios/s13_ej1_evaluacion_e2e.py
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import DATOS, RAIZ, llm  # noqa: E402

LINEA_BASE = RAIZ / "salidas" / "linea_base.json"


class Veredicto(BaseModel):
    puntuacion: int = Field(ge=0, le=2, description="0 incorrecta, 1 parcial, 2 correcta")
    motivo: str


def percentil(valores: list[float], p: float) -> float:
    """Percentil ``p`` (0-100) con interpolación lineal entre los valores ordenados (como ``numpy.percentile``).
    Con 3 decimales; 0.0 si la lista está vacía."""
    raise NotImplementedError("Completa este bloque")


def juzgar(entrada: str, esperado: str, respuesta: str) -> Veredicto:
    """LLM como juez: compara la respuesta con la esperada (temperatura 0, salida ``Veredicto``)."""
    raise NotImplementedError("Completa este bloque")


def evaluar(asistente: Callable[[str], str], casos: list[dict]) -> list[dict]:
    """Ejecuta cada caso midiendo la latencia y lo juzga. Una fila por caso:
    ``{"id", "tipo", "puntuacion", "motivo", "segundos", "respuesta"}`` (segundos con 2 decimales).
    Si el asistente lanza una excepción, puntuación 0 y motivo «ERROR: …» (sin llamar al juez)."""
    raise NotImplementedError("Completa este bloque")


def metricas(filas: list[dict]) -> dict:
    """``{"casos", "exactitud" (% de puntuación 2, 1 decimal), "puntuacion_media" (sobre 2, 2 decimales),
    "latencia_p50", "latencia_p95", "por_tipo": {tipo: exactitud}}``."""
    raise NotImplementedError("Completa este bloque")


def regresiones(actual: dict, base: dict, tolerancia: float = 5.0, factor_latencia: float = 1.5) -> list[str]:
    """Empeoramientos frente a la línea base:

    - «exactitud: 80.0 → 70.0» si la exactitud baja más de ``tolerancia`` puntos.
    - «latencia_p95: 2.0 → 3.5» si la p95 supera ``base × factor_latencia``.
    - «tipo <t>: 100.0 → 50.0» por cada tipo cuya exactitud baja más de ``tolerancia``.
    """
    raise NotImplementedError("Completa este bloque")


def guardar_linea_base(m: dict, ruta: Path = LINEA_BASE) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    from comun.agente import AgenteReAct
    from comun.herramientas import buscar_documentacion, esquema_buscar_documentacion
    from equipos.e2_infrapilot.herramientas import validar_peticion  # noqa: F401  (para que el equipo 2 lo amplíe)

    with (DATOS / "evaluacion" / "golden_e2_infrapilot.jsonl").open(encoding="utf-8") as f:
        casos = [json.loads(l) for l in f if l.strip()]
    agente = lambda entrada: AgenteReAct({"buscar_documentacion": buscar_documentacion}, [esquema_buscar_documentacion()],  # noqa: E731
                                         "Eres InfraPilot. Consulta la documentación y nunca apliques cambios.", nombre_traza="s13_eval").ejecutar(entrada).respuesta
    filas = evaluar(agente, casos)
    m = metricas(filas)
    print(json.dumps(m, indent=2, ensure_ascii=False))
    if LINEA_BASE.exists():
        print("Regresiones:", regresiones(m, json.loads(LINEA_BASE.read_text(encoding="utf-8"))) or "ninguna")
    else:
        guardar_linea_base(m)
        print("Línea base guardada en", LINEA_BASE)
