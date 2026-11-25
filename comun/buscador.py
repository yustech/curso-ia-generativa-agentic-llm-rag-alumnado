"""Buscador semántico de referencia con caché de embeddings en disco.

Lo usan los laboratorios a partir de la sesión 7 (agentes que consultan la
documentación) y los asistentes de los equipos como punto de partida.

    from comun.buscador import BuscadorSemantico
    buscador = BuscadorSemantico.de_documentos()
    for trozo, puntuacion in buscador.buscar("¿Cuántos días de vacaciones hay?", k=3):
        print(puntuacion, trozo.referencia)
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from comun import RAIZ, llm
from comun.documentos import CARPETA_DOCUMENTOS, Trozo, cargar_trozos

CARPETA_CACHE = RAIZ / "indices"


class BuscadorSemantico:
    def __init__(self, trozos: list[Trozo], cache: Path | None = None) -> None:
        self.trozos = trozos
        self.matriz = self._vectores(trozos, cache)

    @classmethod
    def de_documentos(cls, carpeta: Path = CARPETA_DOCUMENTOS, usar_cache: bool = True) -> "BuscadorSemantico":
        trozos = cargar_trozos(carpeta)
        modelo = "llm-falso" if llm.es_falso() else llm.MODELO_EMBEDDINGS
        huella = hashlib.sha256((modelo + "".join(t.texto for t in trozos)).encode()).hexdigest()[:12]
        cache = CARPETA_CACHE / f"embeddings_{huella}.json" if usar_cache and not llm.es_falso() else None
        return cls(trozos, cache)

    @staticmethod
    def _vectores(trozos: list[Trozo], cache: Path | None) -> np.ndarray:
        if cache and cache.exists():
            vectores = json.loads(cache.read_text(encoding="utf-8"))
        else:
            vectores = llm.embeddings([t.texto for t in trozos]) if trozos else []
            if cache:
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(vectores), encoding="utf-8")
        matriz = np.array(vectores, dtype=float)
        if matriz.size:
            matriz /= np.linalg.norm(matriz, axis=1, keepdims=True)
        return matriz

    def buscar(self, consulta: str, k: int = 4) -> list[tuple[Trozo, float]]:
        if not self.trozos:
            return []
        vector = np.array(llm.embeddings(consulta)[0], dtype=float)
        vector /= np.linalg.norm(vector) or 1.0
        puntuaciones = self.matriz @ vector
        orden = np.argsort(-puntuaciones)[:k]
        return [(self.trozos[i], round(float(puntuaciones[i]), 4)) for i in orden]


def contexto_numerado(resultados: list[tuple[Trozo, float]]) -> str:
    """Bloques ``[n] documento › sección`` listos para pegar en un prompt."""
    return "\n\n".join(f"[{i}] {t.referencia}\n{t.texto}" for i, (t, _) in enumerate(resultados, 1))
