"""Utilidades comunes del curso: cliente LLM, trazas y acceso a los datos de Atlántica."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "datos" / "atlantica"
