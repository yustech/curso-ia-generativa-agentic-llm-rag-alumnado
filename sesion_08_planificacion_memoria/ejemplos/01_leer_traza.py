"""Ejemplo 1: imprimir una traza de forma legible.

    python sesion_08_planificacion_memoria/ejemplos/01_leer_traza.py trazas/s08_react.jsonl
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun.trazas import leer  # noqa: E402

fichero = sys.argv[1] if len(sys.argv) > 1 else "trazas/s08_react.jsonl"
ejecucion = None
for paso in leer(fichero):
    if paso["ejecucion"] != ejecucion:
        ejecucion = paso["ejecucion"]
        print(f"\n===== Ejecución {ejecucion} =====")
    if paso["tipo"] == "inicio":
        print(f"OBJETIVO: {paso['objetivo']}")
    elif paso["tipo"] == "modelo":
        print(f"  MODELO decide: {', '.join(paso['herramientas']) or 'responder'}")
    elif paso["tipo"] == "herramienta":
        resultado = " ".join(paso["resultado"].split())
        print(f"  HERRAMIENTA {paso['herramienta']}({paso['argumentos']})\n     → {resultado[:200]}")
    elif paso["tipo"] == "fin":
        print(f"FIN: {paso['motivo']}")
