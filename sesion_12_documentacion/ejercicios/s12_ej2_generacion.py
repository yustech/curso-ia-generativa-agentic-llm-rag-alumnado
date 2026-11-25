"""Sesión 12 - Ejercicio 2: generación documental controlada (informe de estado).

Las cifras, el semáforo y la estructura los pone el código; el LLM solo redacta el
resumen, y cada dato del resumen debe salir de los datos que se le pasan.

    python sesion_12_documentacion/ejercicios/s12_ej2_generacion.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

SECCIONES = ["1. Resumen", "2. Semáforo", "3. Avance del sprint", "4. Hitos próximos",
             "5. Riesgos y problemas abiertos", "6. Decisiones que se necesitan de dirección"]


@dataclass
class DatosInforme:
    proyecto: str
    semana: str
    sprint: int
    comprometidos: int
    completados: int
    desviacion_plazo: float
    desviacion_coste: float
    hitos: list[tuple[str, str, str]] = field(default_factory=list)       # (hito, fecha, estado)
    riesgos: list[tuple[str, int, int]] = field(default_factory=list)     # (descripción, P, I)
    decisiones: list[str] = field(default_factory=list)
    fuentes: list[str] = field(default_factory=list)


def semaforo(desviacion: float, hito_en_peligro: bool = False) -> str:
    """Verde (≤ 5 %), Ámbar (≤ 15 %) o Rojo (> 15 % o hito crítico en peligro), según ATL-PMO-009."""
    raise NotImplementedError("Completa este bloque")


def semaforo_general(datos: DatosInforme) -> str:
    """El peor color entre plazo (con hito en peligro si algún hito está «En riesgo») y coste."""
    raise NotImplementedError("Completa este bloque")


def resumen_con_llm(datos: DatosInforme) -> str:
    """Pide al LLM un resumen de exactamente tres líneas usando SOLO los datos (temperatura 0)."""
    riesgos = "; ".join(f"{d} (exposición {p * i})" for d, p, i in datos.riesgos)
    hitos = "; ".join(f"{h} el {f} ({e})" for h, f, e in datos.hitos)
    return llm.chat(
        f"Proyecto {datos.proyecto}, semana {datos.semana}. Sprint {datos.sprint}: {datos.completados} de "
        f"{datos.comprometidos} puntos. Hitos: {hitos}. Riesgos: {riesgos}. Decisiones pendientes: {'; '.join(datos.decisiones)}.\n\n"
        "Escribe un resumen ejecutivo de exactamente tres líneas usando solo estos datos.", temperatura=0)


def generar_informe(datos: DatosInforme, resumen: str) -> str:
    """Informe en Markdown con las seis ``SECCIONES`` (como títulos ``## ``) en orden:

    1. El resumen recibido.
    2. Tabla | General | Plazo | Coste | con los semáforos.
    3. «X de Y puntos completados (Z %).» (Z sin decimales; 0 % si no hay comprometidos).
    4. Tabla | Hito | Fecha | Estado |.
    5. Tabla | Riesgo | P | I | Exposición | ¿Escalar? | («Sí» si exposición ≥ 15), ordenada por exposición descendente.
    6. Viñetas con las decisiones, o «Ninguna.».
    Termina con «Fuentes: a, b.» si hay fuentes. Empieza con «# Informe de estado · <proyecto> · <semana>».
    """
    raise NotImplementedError("Completa este bloque")


DATOS_EJEMPLO = DatosInforme(
    proyecto="Faro 2.0", semana="23 al 27 de noviembre de 2026", sprint=22, comprometidos=34, completados=30,
    desviacion_plazo=8, desviacion_coste=2,
    hitos=[("Congelación de alcance del piloto", "11/12/2026", "En plazo"), ("Piloto con 20 tiendas de Nortia", "15/01/2027", "En riesgo")],
    riesgos=[("Plazo ajustado del piloto por Navidad y congelación de cambios", 4, 4),
             ("Ausencia de la única diseñadora del 9 al 20 de diciembre", 5, 3),
             ("Equipo de diseño de una sola persona", 2, 3)],
    decisiones=["Confirmar el apoyo del equipo de diseño del portal de empleados"],
    fuentes=["2026-11-24_seguimiento_faro2.md", "informe_estado_2026-11-20.md"])

if __name__ == "__main__":
    print(generar_informe(DATOS_EJEMPLO, resumen_con_llm(DATOS_EJEMPLO)))
