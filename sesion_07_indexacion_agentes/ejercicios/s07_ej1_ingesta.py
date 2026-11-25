"""Sesión 7 - Ejercicio 1: pipeline de ingesta incremental.

Solo se reprocesan los documentos nuevos o modificados, y se borran del índice
los eliminados. Así un índice de miles de documentos se mantiene al día en
segundos en lugar de reconstruirse entero cada noche.

    python sesion_07_indexacion_agentes/ejercicios/s07_ej1_ingesta.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import chromadb

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import RAIZ, llm  # noqa: E402
from comun.documentos import CARPETA_DOCUMENTOS, Documento, cargar_documentos, trocear_por_secciones  # noqa: E402


def huella(texto: str) -> str:
    """Primeros 16 caracteres del SHA-256 del texto (UTF-8)."""
    raise NotImplementedError("Completa este bloque")


def clasificar_cambios(documentos: list[Documento], manifiesto: dict[str, str]) -> dict[str, list[str]]:
    """Compara los documentos actuales con el manifiesto ``{nombre: huella}`` de la última ingesta.

    Devuelve ``{"nuevos": [...], "modificados": [...], "eliminados": [...], "sin_cambios": [...]}``
    con nombres de documento ordenados alfabéticamente en cada lista.
    """
    raise NotImplementedError("Completa este bloque")


class PipelineIngesta:
    """Ingesta incremental sobre una colección Chroma con un manifiesto JSON."""

    def __init__(self, carpeta_indice: Path | str = RAIZ / "indices" / "ingesta", nombre: str = "atlantica") -> None:
        self.carpeta = Path(carpeta_indice)
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self.ruta_manifiesto = self.carpeta / f"{nombre}_manifiesto.json"
        cliente = chromadb.PersistentClient(path=str(self.carpeta / "chroma"))
        self.coleccion = cliente.get_or_create_collection(nombre, embedding_function=None,
                                                          configuration={"hnsw": {"space": "cosine"}})

    def leer_manifiesto(self) -> dict[str, str]:
        return json.loads(self.ruta_manifiesto.read_text(encoding="utf-8")) if self.ruta_manifiesto.exists() else {}

    def borrar_documento(self, nombre: str) -> None:
        """Borra de la colección todos los trozos cuyo metadato ``documento`` es ``nombre``."""
        raise NotImplementedError("Completa este bloque")

    def indexar_documento(self, documento: Documento) -> int:
        """Trocea por secciones, calcula los embeddings en una llamada y hace ``upsert`` con metadatos
        ``{"documento", "seccion", "huella"}`` más los metadatos del trozo. Devuelve el número de trozos."""
        raise NotImplementedError("Completa este bloque")

    def procesar(self, carpeta: Path | str = CARPETA_DOCUMENTOS) -> dict:
        """Ejecuta una ingesta incremental y guarda el manifiesto actualizado.

        - Nuevos: se indexan. Modificados: se borran sus trozos y se vuelven a indexar.
        - Eliminados: se borran. Sin cambios: no se tocan.

        Devuelve ``{"nuevos": n, "modificados": n, "eliminados": n, "sin_cambios": n,
        "trozos_indexados": n, "total": elementos de la colección}``.
        """
        raise NotImplementedError("Completa este bloque")

    def buscar(self, pregunta: str, k: int = 4) -> list[tuple[str, str, float]]:
        """``(documento, seccion, similitud)`` de los ``k`` trozos más parecidos."""
        r = self.coleccion.query(query_embeddings=llm.embeddings(pregunta), n_results=k)
        return [(m["documento"], m["seccion"], round(1 - d, 4)) for m, d in zip(r["metadatas"][0], r["distances"][0])]


if __name__ == "__main__":
    pipeline = PipelineIngesta()
    print("Primera ingesta:", pipeline.procesar())
    print("Segunda ingesta (nada cambia):", pipeline.procesar())
    print(pipeline.buscar("¿Cuántos días se conservan las copias en producción?", 2))
