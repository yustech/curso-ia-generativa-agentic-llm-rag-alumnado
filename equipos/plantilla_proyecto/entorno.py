"""Conecta el proyecto del equipo con el repositorio del curso.

Importad este módulo antes que nada (``import entorno``): carga el ``.env`` y
añade al ``sys.path`` la carpeta del curso para poder usar ``comun`` y
``equipos.<reto>.herramientas`` (los sistemas simulados del cliente).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

RAIZ_PROYECTO = Path(__file__).resolve().parent
load_dotenv(RAIZ_PROYECTO / ".env")


def _buscar_curso() -> Path:
    configurada = os.getenv("CURSO_RAIZ")
    if configurada:
        ruta = Path(configurada)
        ruta = ruta if ruta.is_absolute() else (RAIZ_PROYECTO / ruta)
        candidatos = [ruta.resolve()]
    else:
        # Sin configurar: se busca hacia arriba (sirve para probar la plantilla dentro del curso).
        candidatos = list(RAIZ_PROYECTO.parents)
    for candidato in candidatos:
        if (candidato / "comun" / "llm.py").is_file():
            return candidato
    raise RuntimeError(
        "No encuentro el repositorio del curso. Define CURSO_RAIZ en el .env con la ruta a "
        "curso-ia-generativa-agentic-llm-rag-alumnado (puede ser relativa a este proyecto)."
    )


CURSO_RAIZ = _buscar_curso()
if str(CURSO_RAIZ) not in sys.path:
    sys.path.insert(1, str(CURSO_RAIZ))
CARPETA_SALIDAS = RAIZ_PROYECTO / "salidas"
