"""Sesión 12 - Ejercicio 1: de las actas a JSON validado y trazable.

    python sesion_12_documentacion/ejercicios/s12_ej1_extraccion.py
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import DATOS, llm  # noqa: E402

CARPETA_ACTAS = DATOS / "proyectos" / "actas"
MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
         "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}


class Accion(BaseModel):
    descripcion: str
    responsable: str = Field(description="Nombre de la persona responsable tal como aparece en el acta")
    fecha: str | None = Field(default=None, description="Fecha límite tal como aparece en el acta, o null")


class Riesgo(BaseModel):
    descripcion: str
    probabilidad: int | None = Field(default=None, ge=1, le=5)
    impacto: int | None = Field(default=None, ge=1, le=5)


class Acta(BaseModel):
    fecha: str = Field(description="Fecha de la reunión tal como aparece en el acta")
    asistentes: list[str]
    decisiones: list[str]
    acciones: list[Accion]
    riesgos: list[Riesgo]


SISTEMA = ("Extraes información de actas de reunión de Atlántica Logística. Usa solo lo que dice el acta: "
           "si un dato no aparece, usa null o una lista vacía. No inventes responsables ni fechas. "
           "Copia los nombres y las fechas tal como aparecen.")


def _normal(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def normalizar_fecha(texto: str | None, anio: int = 2026) -> str | None:
    """Fecha en formato ISO ``AAAA-MM-DD`` a partir de «3 de noviembre de 2026», «10/11/2026», «25/11»
    (con el año por defecto) o «2026-11-03». Devuelve None si no se reconoce o el texto es None."""
    raise NotImplementedError("Completa este bloque")


def extraer_acta(texto: str) -> Acta:
    """Extrae el acta con ``llm.estructurado`` y ``SISTEMA`` y normaliza a ISO la fecha de la reunión y las de
    las acciones (si una fecha no se reconoce, se deja como estaba)."""
    raise NotImplementedError("Completa este bloque")


def aparece(nombre: str, texto: str) -> bool:
    """True si alguna palabra de más de 2 letras del nombre aparece en el texto (sin mayúsculas ni tildes).
    «Lucía Prieto» aparece en un acta que solo dice «Lucía»."""
    raise NotImplementedError("Completa este bloque")


def problemas_trazabilidad(acta: Acta, texto: str) -> list[str]:
    """Datos extraídos que no se pueden rastrear en el texto original:

    - «Asistente no encontrado: X», «Responsable no encontrado: X» (según ``aparece``).
    - «Riesgo sin probabilidad o impacto: <descripción>» si falta alguno de los dos.
    """
    raise NotImplementedError("Completa este bloque")


def procesar_carpeta(carpeta: Path = CARPETA_ACTAS) -> dict[str, dict]:
    """``{nombre_fichero: {"acta": Acta, "problemas": [...]}}`` para cada ``.md`` de la carpeta."""
    resultados = {}
    for ruta in sorted(Path(carpeta).glob("*.md")):
        texto = ruta.read_text(encoding="utf-8")
        acta = extraer_acta(texto)
        resultados[ruta.name] = {"acta": acta, "problemas": problemas_trazabilidad(acta, texto)}
    return resultados


if __name__ == "__main__":
    for nombre, r in procesar_carpeta().items():
        acta = r["acta"]
        print(f"\n## {nombre} · {acta.fecha} · {len(acta.acciones)} acciones · {len(acta.riesgos)} riesgos")
        for a in acta.acciones:
            print(f"  - {a.responsable}: {a.descripcion} ({a.fecha})")
        print("  Problemas de trazabilidad:", r["problemas"] or "ninguno")
