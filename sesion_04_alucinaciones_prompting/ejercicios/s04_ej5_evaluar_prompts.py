"""Sesión 4 - Ejercicio 5: evaluar y comparar versiones de un prompt.

    python sesion_04_alucinaciones_prompting/ejercicios/s04_ej5_evaluar_prompts.py
"""

from __future__ import annotations

import json
import statistics
import sys
import unicodedata
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

PALABRAS_VACIAS = {"para", "como", "cada", "este", "esta", "estos", "estas", "debe", "pero", "porque", "según",
                   "sobre", "entre", "desde", "hasta", "también", "cuando", "donde", "solo", "sólo", "tiene",
                   "están", "están", "será", "sido", "hace", "otra", "otro", "antes", "después", "nunca"}


def cargar_golden(ruta: Path | str) -> list[dict]:
    """Lee un conjunto dorado en JSONL."""
    raise NotImplementedError("Completa este bloque")


def _normal(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def palabras_clave(texto: str) -> set[str]:
    """Palabras de más de 3 caracteres, en minúsculas y sin tildes, sin signos de puntuación
    en los extremos y que no estén en ``PALABRAS_VACIAS`` (comparadas también sin tildes)."""
    raise NotImplementedError("Completa este bloque")


def puntuar(respuesta: str, esperado: str) -> float:
    """Fracción de palabras clave del texto esperado que aparecen en la respuesta (2 decimales).
    Si el esperado no tiene palabras clave, 1.0."""
    raise NotImplementedError("Completa este bloque")


def evaluar_version(nombre: str, responder: Callable[[str], str], casos: list[dict]) -> dict:
    """Ejecuta ``responder(caso["entrada"])`` en todos los casos y devuelve
    ``{"version": nombre, "media": media con 2 decimales, "por_caso": {id: puntuación}}``."""
    raise NotImplementedError("Completa este bloque")


def comparar(resultados: list[dict]) -> str:
    """Tabla Markdown | Versión | Media | ordenada de mejor a peor, y una última línea «Mejor: <versión>»."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[2]
    casos = cargar_golden(raiz / "datos" / "atlantica" / "evaluacion" / "golden_e2_infrapilot.jsonl")
    politica = (raiz / "datos" / "atlantica" / "documentos" / "06_politica_infraestructura_cloud.md").read_text(encoding="utf-8")
    v1 = lambda entrada: llm.chat(entrada, temperatura=0)  # noqa: E731
    v2 = lambda entrada: llm.chat(entrada, temperatura=0, sistema=(  # noqa: E731
        "Eres el asistente de infraestructura de Atlántica. Responde según esta política y cítala:\n" + politica))
    print(comparar([evaluar_version("v1 sin contexto", v1, casos), evaluar_version("v2 con política", v2, casos)]))
