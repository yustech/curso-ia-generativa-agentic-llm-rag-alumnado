"""Registro de trazas en JSONL.

Una traza es una línea JSON por paso: qué entró, qué salió, cuánto tardó y si
hubo error. Leer trazas es la forma de depurar un sistema con LLM: sin ellas no
se sabe por qué el agente hizo lo que hizo.
"""

from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

CARPETA = Path(__file__).resolve().parent.parent / "trazas"


class Traza:
    """Escribe los pasos de una ejecución en ``trazas/<nombre>.jsonl``."""

    def __init__(self, nombre: str, carpeta: Path | None = None) -> None:
        self.id = uuid.uuid4().hex[:8]
        self.carpeta = carpeta or CARPETA
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self.fichero = self.carpeta / f"{nombre}.jsonl"
        self.pasos: list[dict[str, Any]] = []

    def registrar(self, tipo: str, **datos: Any) -> dict[str, Any]:
        paso = {"ejecucion": self.id, "momento": datetime.now().isoformat(timespec="seconds"), "tipo": tipo, **datos}
        self.pasos.append(paso)
        with self.fichero.open("a", encoding="utf-8") as f:
            f.write(json.dumps(paso, ensure_ascii=False, default=str) + "\n")
        return paso

    @contextmanager
    def paso(self, tipo: str, **datos: Any) -> Iterator[dict[str, Any]]:
        """Mide un paso y registra su resultado o su error."""
        inicio = time.perf_counter()
        resultado: dict[str, Any] = {}
        try:
            yield resultado
            self.registrar(tipo, segundos=round(time.perf_counter() - inicio, 3), **datos, **resultado)
        except Exception as error:  # se registra y se vuelve a lanzar
            self.registrar(tipo, segundos=round(time.perf_counter() - inicio, 3), error=repr(error), **datos)
            raise


def leer(fichero: Path | str) -> list[dict[str, Any]]:
    """Lee un fichero de trazas."""
    with Path(fichero).open(encoding="utf-8") as f:
        return [json.loads(linea) for linea in f if linea.strip()]
