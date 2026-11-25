"""Sesión 1 - Ejercicio 2: pedir la clasificación a un LLM y compararla con la tuya."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

PARADIGMAS = ("reglas_optimizacion", "ml_supervisado", "ml_no_supervisado", "deep_learning_vision", "ia_generativa", "agente")


class Clasificacion(BaseModel):
    """Salida estructurada que debe devolver el modelo."""

    paradigma: Literal["reglas_optimizacion", "ml_supervisado", "ml_no_supervisado", "deep_learning_vision", "ia_generativa", "agente"]
    tipo_modelo: str
    justificacion: str


SISTEMA = (
    "Eres un consultor experto en inteligencia artificial aplicada a empresas. "
    "Clasificas casos de uso según el paradigma técnico más adecuado y justificas en una frase."
)


def construir_prompt(caso: str) -> str:
    """Construye el mensaje para el modelo.

    Debe incluir el caso, la lista de paradigmas posibles (los de ``PARADIGMAS``)
    y pedir una respuesta en JSON con los campos paradigma, tipo_modelo y justificacion.
    """
    raise NotImplementedError("Completa este bloque")


def clasificar_con_llm(caso: str) -> Clasificacion:
    """Pide al modelo la clasificación de un caso y la devuelve validada."""
    raise NotImplementedError("Completa este bloque")


def comparar(manual: dict[str, dict], automatica: dict[str, dict]) -> dict:
    """Compara dos fichas por paradigma.

    Devuelve ``{"coincidencias": int, "total": int, "porcentaje": float, "discrepancias": [ids]}``.
    El porcentaje va de 0 a 100 con un decimal. Solo cuentan los casos presentes en ambas.
    """
    raise NotImplementedError("Completa este bloque")


def main() -> None:
    from s01_ej1_clasificacion import cargar_casos, clasificacion_manual

    casos = cargar_casos()
    automatica = {}
    for caso in casos:
        resultado = clasificar_con_llm(caso["caso"])
        automatica[caso["id"]] = resultado.model_dump()
        print(f"{caso['id']}: {resultado.paradigma:22} {resultado.tipo_modelo}")
    print("\nComparación con tu ficha:", comparar(clasificacion_manual(), automatica))


if __name__ == "__main__":
    main()
