"""Sesión 5 - Ejercicio 1: cargar y trocear documentos.

    python sesion_05_rag_arquitectura/ejercicios/s05_ej1_documentos.py
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from pathlib import Path

CARPETA = Path(__file__).resolve().parents[2] / "datos" / "atlantica" / "documentos"


@dataclass
class Documento:
    nombre: str
    titulo: str
    texto: str
    metadatos: dict[str, str] = field(default_factory=dict)


@dataclass
class Trozo:
    id: str
    documento: str
    seccion: str
    texto: str


def leer_front_matter(texto: str) -> tuple[dict[str, str], str]:
    """Separa la cabecera de metadatos del cuerpo.

    La cabecera empieza con una línea ``---`` al principio del texto y termina en la siguiente
    línea ``---``. Cada línea intermedia es ``clave: valor`` (el valor puede contener «:»).
    Devuelve ``(metadatos, cuerpo)``, con el cuerpo sin saltos de línea iniciales.
    Si no hay cabecera, devuelve ``({}, texto)``.
    """
    raise NotImplementedError("Completa este bloque")


def cargar_documentos(carpeta: Path = CARPETA) -> list[Documento]:
    """Carga los ``.md`` de la carpeta en orden alfabético. El título es el campo ``titulo`` de la
    cabecera; si no existe, el nombre del fichero sin extensión."""
    raise NotImplementedError("Completa este bloque")


def trocear_por_caracteres(texto: str, tamano: int, solape: int) -> list[str]:
    """Trozos de ``tamano`` caracteres; cada uno empieza ``tamano - solape`` caracteres después del anterior.
    El último trozo puede ser más corto. Se descartan trozos vacíos o solo con espacios.
    Lanza ``ValueError`` si ``tamano <= 0``, ``solape < 0`` o ``solape >= tamano``.
    """
    raise NotImplementedError("Completa este bloque")


def trocear_por_secciones(documento: Documento) -> list[Trozo]:
    """Un trozo por cada sección que empieza con ``## ``.

    - El texto anterior a la primera sección (sin contar la línea del título ``# ``) forma la sección «Introducción», si no está vacío.
    - Cada trozo tiene ``id`` = ``<nombre sin extensión>#<n>`` (n empieza en 0), ``documento`` = nombre del fichero,
      ``seccion`` = título de la sección sin ``## `` y ``texto`` = ``"<titulo del documento> — <seccion>\\n\\n<contenido>"``.
    - El contenido no incluye la línea del título de la sección y no tiene espacios en los extremos.
    - Se omiten las secciones sin contenido.
    """
    raise NotImplementedError("Completa este bloque")


def estadisticas(textos: list[str]) -> dict[str, float]:
    """``{"n", "media", "minimo", "maximo"}`` de las longitudes en caracteres (media con 1 decimal)."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    documentos = cargar_documentos()
    por_secciones = [t.texto for d in documentos for t in trocear_por_secciones(d)]
    por_caracteres = [t for d in documentos for t in trocear_por_caracteres(d.texto, 800, 100)]
    print(f"{len(documentos)} documentos")
    print("Por secciones:   ", estadisticas(por_secciones))
    print("Por caracteres:  ", estadisticas(por_caracteres))
    print("\nEjemplo de trozo por secciones:\n", por_secciones[5][:400])
    print("\nEjemplo de trozo por caracteres:\n", por_caracteres[5][:400])
