"""Sesión 4 - Ejercicio 4: salida estructurada validada y reglas de negocio.

    python sesion_04_alucinaciones_prompting/ejercicios/s04_ej4_salida_estructurada.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402


class ClasificacionIncidencia(BaseModel):
    """Clasificación de una incidencia según el procedimiento ATL-OPS-010."""

    categoria: Literal["transporte", "almacén", "sistemas"]
    prioridad: Literal["P1", "P2", "P3", "P4"]
    resumen: str = Field(max_length=120)
    requiere_humano: bool


SISTEMA = (
    "Clasificas incidencias de Atlántica Logística según su procedimiento de gestión de incidencias.\n"
    "Prioridades: P1 = servicio crítico (Faro, Puerto o portal de clientes) caído para todos; "
    "P2 = servicio degradado o caído para un centro o un cliente importante; "
    "P3 = fallo con alternativa disponible; P4 = consulta o mejora menor.\n"
    "requiere_humano es true si la prioridad es P1 o P2. El resumen tiene como máximo 120 caracteres."
)


def clasificar(texto: str) -> ClasificacionIncidencia:
    """Clasifica la incidencia con ``llm.estructurado`` usando ``SISTEMA``."""
    raise NotImplementedError("Completa este bloque")


def problemas_de_negocio(c: ClasificacionIncidencia) -> list[str]:
    """Reglas que el esquema no puede comprobar. Devuelve los textos de las reglas incumplidas:

    - «P1 y P2 requieren intervención humana» si es P1 o P2 y ``requiere_humano`` es False.
    - «P3 y P4 no deberían escalar» si es P3 o P4 y ``requiere_humano`` es True.
    - «Resumen vacío» si el resumen está vacío o solo tiene espacios.
    """
    raise NotImplementedError("Completa este bloque")


def corregir(c: ClasificacionIncidencia) -> ClasificacionIncidencia:
    """Devuelve una copia con ``requiere_humano`` coherente con la prioridad (P1/P2 → True; P3/P4 → False)."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    for texto in ["Faro está caído en todos los centros desde las 8:00.",
                  "La impresora de etiquetas de Bilbao falla, pero se puede usar la de la oficina.",
                  "¿Se puede cambiar el color del botón de descarga del portal?"]:
        c = clasificar(texto)
        print(c.model_dump(), problemas_de_negocio(c))
