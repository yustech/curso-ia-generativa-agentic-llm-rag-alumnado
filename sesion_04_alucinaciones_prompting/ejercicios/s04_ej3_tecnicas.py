"""Sesión 4 - Ejercicio 3: zero-shot, few-shot y cadena de pensamiento.

    python sesion_04_alucinaciones_prompting/ejercicios/s04_ej3_tecnicas.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

CATEGORIAS = ["transporte", "almacén", "sistemas"]
EJEMPLOS = [
    ("El camión 4312 lleva dos horas parado en la AP-9", "transporte"),
    ("Faltan 12 palés en la ubicación B-14", "almacén"),
    ("Faro no carga la lista de envíos", "sistemas"),
]


def normalizar_categoria(texto: str) -> str | None:
    """Primera categoría de ``CATEGORIAS`` que aparece en el texto (en minúsculas), o None."""
    raise NotImplementedError("Completa este bloque")


def zero_shot(incidencia: str) -> str | None:
    """Clasifica la incidencia sin ejemplos, con temperatura 0. Devuelve la categoría normalizada."""
    raise NotImplementedError("Completa este bloque")


def mensajes_few_shot(incidencia: str) -> list[dict]:
    """Mensajes: uno de sistema con la instrucción y las categorías, un par user/assistant por
    cada ejemplo de ``EJEMPLOS`` y, al final, la incidencia como mensaje user."""
    raise NotImplementedError("Completa este bloque")


def few_shot(incidencia: str) -> str | None:
    """Clasifica con los mensajes few-shot y temperatura 0."""
    raise NotImplementedError("Completa este bloque")


def extraer_respuesta_final(texto: str) -> str:
    """Devuelve lo que va detrás de la ÚLTIMA aparición de «Respuesta final:» (sin distinguir
    mayúsculas), sin espacios en los extremos. Si no aparece, devuelve la última línea no vacía."""
    raise NotImplementedError("Completa este bloque")


def con_razonamiento(pregunta: str) -> tuple[str, str]:
    """Pide razonar paso a paso y terminar con «Respuesta final: …». Devuelve ``(texto_completo, respuesta_final)``."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    for incidencia in ["La carretilla del pasillo 3 no arranca", "El portal da error 500 al descargar albaranes",
                       "Retraso en Burgos por un pinchazo"]:
        print(f"{incidencia[:45]:46} zero-shot={zero_shot(incidencia)}  few-shot={few_shot(incidencia)}")
    pregunta = ("Un envío en rígido recorre 120 km con 1.500 kg. El precio es 0,95 €/km más 0,02 € por kg por encima "
                "de 1.000 kg y por cada 100 km. ¿Cuál es el precio base antes de recargos?")
    _, respuesta = con_razonamiento(pregunta)
    print("\nCon razonamiento:", respuesta, "(correcto: 126 €)")
