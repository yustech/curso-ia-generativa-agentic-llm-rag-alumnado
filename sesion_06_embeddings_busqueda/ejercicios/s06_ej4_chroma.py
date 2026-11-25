"""Sesión 6 - Ejercicio 4: base vectorial persistente con Chroma.

    python sesion_06_embeddings_busqueda/ejercicios/s06_ej4_chroma.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import chromadb

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402
from comun.documentos import Trozo  # noqa: E402

RUTA = Path(__file__).resolve().parents[2] / "indices" / "chroma"


def crear_coleccion(ruta: Path | str = RUTA, nombre: str = "atlantica"):
    """Cliente persistente en ``ruta`` y colección con distancia coseno, SIN función de embeddings
    propia de Chroma (``embedding_function=None``)."""
    raise NotImplementedError("Completa este bloque")


def indexar(coleccion, trozos: list[Trozo], lote: int = 64) -> int:
    """Calcula los embeddings con ``llm.embeddings`` y hace ``upsert`` por lotes con:
    ids = ``trozo.id``, documents = ``trozo.texto``, embeddings y metadatas ``{"documento", "seccion"}``
    más los ``trozo.metadatos``. Devuelve el número de elementos de la colección al terminar."""
    raise NotImplementedError("Completa este bloque")


def consultar(coleccion, pregunta: str, k: int = 4, documento: str | None = None) -> list[dict]:
    """Consulta con el embedding de la pregunta. Si se indica ``documento``, filtra por ese metadato.

    Devuelve una lista de ``{"id", "documento", "seccion", "similitud", "texto"}`` donde
    ``similitud = 1 - distancia`` redondeada a 4 decimales.
    """
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    from comun.documentos import cargar_trozos

    coleccion = crear_coleccion()
    print("Elementos indexados:", indexar(coleccion, cargar_trozos()))
    for r in consultar(coleccion, "¿Qué tipos de instancia están permitidos?", k=3):
        print(r["similitud"], r["documento"], "›", r["seccion"])
    print("\nSolo en el catálogo de módulos:")
    for r in consultar(coleccion, "¿Cuánto cuesta una máquina?", k=2, documento="07_catalogo_modulos_terraform.md"):
        print(r["similitud"], r["seccion"])
