"""Sesión 14 - Ejercicio 1: verificador automático de la entrega del proyecto final.

    python sesion_14_proyecto_final/ejercicios/s14_ej1_verificar_entrega.py <carpeta del repositorio del equipo>
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

DOCUMENTOS = ["README.md", "docs/ficha_agente.md", "docs/canvas_caso_uso.md", "docs/propuesta_tecnica.md",
              "docs/plan_validacion.md", "docs/informe_evaluacion.md"]
TIPOS_GOLDEN = {"normativa", "tarea", "ambigua", "fuera_de_alcance", "seguridad"}
PATRONES_SECRETOS = [r"sk-[A-Za-z0-9]{20,}", r"(?i)(password|contraseña|api_key|secret)\s*=\s*['\"][^'\"]{6,}['\"]",
                     r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"]


def fila(comprobacion: str, ok: bool, detalle: str = "") -> dict:
    return {"comprobacion": comprobacion, "ok": ok, "detalle": detalle}


def comprobar_documentos(raiz: Path) -> list[dict]:
    """Una fila por documento de ``DOCUMENTOS``: existe y tiene al menos 300 caracteres."""
    raise NotImplementedError("Completa este bloque")


def comprobar_golden(raiz: Path, minimo: int = 30) -> dict:
    """``evals/golden_set.jsonl``: al menos ``minimo`` líneas JSON válidas con ``id``, ``entrada`` y ``esperado``,
    y presencia de los cinco tipos de ``TIPOS_GOLDEN`` (campo ``tipo``). El detalle indica los casos válidos y los tipos que faltan."""
    raise NotImplementedError("Completa este bloque")


def contar_pruebas(raiz: Path) -> dict:
    """Número de funciones ``test_*`` en los ``test_*.py`` de ``tests/`` (con ``ast``). Correcto si hay 10 o más."""
    raise NotImplementedError("Completa este bloque")


def buscar_secretos(raiz: Path) -> dict:
    """Correcto si no hay fichero ``.env`` y ningún ``.py``, ``.md``, ``.json``, ``.yml`` o ``.toml`` (fuera de ``.venv``)
    contiene un patrón de ``PATRONES_SECRETOS``. El detalle lista los ficheros problemáticos (rutas relativas con «/»)."""
    raise NotImplementedError("Completa este bloque")


def verificar(raiz: Path | str) -> list[dict]:
    """Todas las comprobaciones: documentos, conjunto dorado, pruebas, secretos, y existencia de ``app.py``,
    ``requirements.txt`` y una carpeta ``rag/``."""
    raise NotImplementedError("Completa este bloque")


def informe(filas: list[dict]) -> str:
    """Tabla | Comprobación | Resultado | Detalle | (✅/❌) y la línea «Entrega completa: sí» o «Entrega completa: no (N pendientes)»."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    carpeta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    print(informe(verificar(carpeta)))
