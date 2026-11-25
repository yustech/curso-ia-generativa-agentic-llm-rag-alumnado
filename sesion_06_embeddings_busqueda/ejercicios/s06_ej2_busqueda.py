"""Sesión 6 - Ejercicio 2: búsqueda léxica (BM25), semántica e híbrida (RRF).

    python sesion_06_embeddings_busqueda/ejercicios/s06_ej2_busqueda.py
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402
from comun.documentos import Trozo, cargar_trozos  # noqa: E402

PALABRAS_VACIAS = set("""a al algo como con de del el en es esta este la las lo los mas me mi muy no o para pero por
que se si sin sobre su sus te tu un una uno y ya cual cuales cuando cuanto cuantos cuantas donde hay puedo tengo""".split())


def tokenizar(texto: str) -> list[str]:
    """Minúsculas, sin tildes (pero conservando la ñ), separando por cualquier carácter que no sea
    letra, dígito, punto o guion; se quitan puntos y guiones de los extremos de cada término y se
    descartan los términos de menos de 2 caracteres y las ``PALABRAS_VACIAS``.

    Ejemplo: ``"¿Qué tipos de instancia, t3.medium o m6i.large?"`` →
    ``["tipos", "instancia", "t3.medium", "m6i.large"]``
    """
    raise NotImplementedError("Completa este bloque")


class BuscadorBM25:
    def __init__(self, trozos: list[Trozo]) -> None:
        """Crea el índice ``BM25Okapi`` con los textos tokenizados de los trozos."""
        self.trozos = trozos
        raise NotImplementedError("Completa este bloque")

    def buscar(self, consulta: str, k: int = 5) -> list[tuple[Trozo, float]]:
        """Los ``k`` trozos con mayor puntuación BM25 (``get_scores``), de mayor a menor."""
        raise NotImplementedError("Completa este bloque")


class BuscadorSemantico:
    def __init__(self, trozos: list[Trozo]) -> None:
        """Calcula y normaliza los embeddings de todos los trozos (una llamada a ``llm.embeddings``)."""
        self.trozos = trozos
        raise NotImplementedError("Completa este bloque")

    def buscar(self, consulta: str, k: int = 5) -> list[tuple[Trozo, float]]:
        """Los ``k`` trozos con mayor similitud coseno, de mayor a menor."""
        raise NotImplementedError("Completa este bloque")


def fusion_rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Reciprocal Rank Fusion de varias listas de ids ordenadas (posición 1 = la primera).

    Devuelve ``(id, puntuación)`` de mayor a menor puntuación; a igualdad, por orden de primera
    aparición (recorriendo los rankings en orden).
    """
    raise NotImplementedError("Completa este bloque")


class BuscadorHibrido:
    def __init__(self, lexico: BuscadorBM25, semantico: BuscadorSemantico, candidatos: int = 20) -> None:
        self.lexico, self.semantico, self.candidatos = lexico, semantico, candidatos
        self.por_id = {t.id: t for t in lexico.trozos}

    def buscar(self, consulta: str, k: int = 5) -> list[tuple[Trozo, float]]:
        """Fusiona con RRF los ``candidatos`` primeros de cada buscador y devuelve los ``k`` mejores."""
        raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    trozos = cargar_trozos()
    bm25, semantico = BuscadorBM25(trozos), BuscadorSemantico(trozos)
    hibrido = BuscadorHibrido(bm25, semantico)
    for consulta in ["¿Cuándo se reúne el CAB?", "ATL-INF-006 etiquetas", "¿Con cuánto tiempo pido los días libres?"]:
        print(f"\n### {consulta}")
        for nombre, buscador in (("BM25", bm25), ("Semántico", semantico), ("Híbrido", hibrido)):
            print(f"{nombre:10}", [t.referencia[:55] for t, _ in buscador.buscar(consulta, 2)])
