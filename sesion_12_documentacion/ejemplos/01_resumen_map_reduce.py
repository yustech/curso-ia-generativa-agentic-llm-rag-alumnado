"""Ejemplo 1: resumen map-reduce de las cuatro actas del proyecto Faro 2.0.

    python sesion_12_documentacion/ejemplos/01_resumen_map_reduce.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import DATOS, llm  # noqa: E402

actas = sorted((DATOS / "proyectos" / "actas").glob("*.md"))

# MAP: un resumen de tres viñetas por acta, citando el acta
parciales = []
for ruta in actas:
    resumen = llm.chat(ruta.read_text(encoding="utf-8"), temperatura=0,
                       sistema="Resume el acta en tres viñetas con decisiones, acciones y riesgos. No inventes datos.")
    parciales.append(f"Acta {ruta.stem}:\n{resumen}")
    print(f"MAP {ruta.name}: {len(resumen)} caracteres")

# REDUCE: un resumen del mes que cita de qué acta sale cada punto
final = llm.chat("\n\n".join(parciales), temperatura=0,
                 sistema="Con estos resúmenes de actas, escribe el resumen del mes para dirección en 5 viñetas. "
                         "Termina cada viñeta con el acta de origen entre paréntesis.")
print("\nREDUCE:\n" + final)
