"""Sesión 1 - Ejercicio 1: clasificar casos de uso por paradigma."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

RUTA_CASOS = Path(__file__).resolve().parents[2] / "datos" / "atlantica" / "casos_uso.json"

PARADIGMAS = (
    "reglas_optimizacion",
    "ml_supervisado",
    "ml_no_supervisado",
    "deep_learning_vision",
    "ia_generativa",
    "agente",
)


def cargar_casos(ruta: Path = RUTA_CASOS) -> list[dict]:
    """Devuelve la lista de casos de uso del fichero JSON."""
    raise NotImplementedError("Completa este bloque")


def clasificacion_manual() -> dict[str, dict]:
    """Tu clasificación de los 8 casos de ``casos_uso.json``.

    Devuelve un diccionario ``{id_caso: {"paradigma", "tipo_modelo", "justificacion"}}``.
    ``paradigma`` debe ser uno de ``PARADIGMAS``.
    """
    # TODO: completa el diccionario con los 8 casos (C1 a C8)
    raise NotImplementedError("Completa este bloque")


def validar_ficha(ficha: dict[str, dict], casos: list[dict] | None = None) -> list[str]:
    """Devuelve la lista de problemas de la ficha (vacía si es correcta).

    Comprueba que están todos los casos, que el paradigma es válido, que hay tipo
    de modelo y que la justificación tiene al menos 20 caracteres.
    """
    raise NotImplementedError("Completa este bloque")


def resumen_por_paradigma(ficha: dict[str, dict]) -> dict[str, int]:
    """Cuenta cuántos casos hay de cada paradigma, en el orden de ``PARADIGMAS``."""
    raise NotImplementedError("Completa este bloque")


def a_markdown(ficha: dict[str, dict], casos: list[dict]) -> str:
    """Devuelve la ficha como tabla Markdown: | Caso | Descripción | Paradigma | Tipo de modelo | Justificación |"""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    casos = cargar_casos()
    ficha = clasificacion_manual()
    problemas = validar_ficha(ficha, casos)
    print("\n".join(problemas) if problemas else "Ficha completa y válida.\n")
    print(a_markdown(ficha, casos))
    print("\nResumen:", resumen_por_paradigma(ficha))
