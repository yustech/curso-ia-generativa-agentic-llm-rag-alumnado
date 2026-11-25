"""Sesión 13 - Ejercicio 4: caso de negocio y viabilidad de una solución de IA."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class CasoNegocio:
    nombre: str
    horas_ahorradas_mes: float      # horas de trabajo que se ahorran al mes (ya descontada la revisión humana)
    coste_hora: float               # € por hora de la persona que hace hoy el trabajo
    coste_implantacion: float       # € de una vez (desarrollo, integración, formación)
    coste_operacion_mes: float      # € al mes (infraestructura, mantenimiento, supervisión)
    riesgo: int                     # 1 (bajo) a 5 (alto): impacto de un error
    madurez_datos: int              # 1 (no hay datos) a 5 (datos listos y de calidad)


def beneficio_mensual(c: CasoNegocio) -> float:
    """Ahorro (horas × coste hora) menos coste de operación, con 2 decimales."""
    raise NotImplementedError("Completa este bloque")


def meses_recuperacion(c: CasoNegocio) -> float:
    """Meses para recuperar la implantación (redondeado hacia arriba a 1 decimal). ``math.inf`` si el beneficio ≤ 0."""
    raise NotImplementedError("Completa este bloque")


def roi_primer_anio(c: CasoNegocio) -> float:
    """(12 × beneficio mensual − implantación) / implantación × 100, con 1 decimal."""
    raise NotImplementedError("Completa este bloque")


def recomendacion(c: CasoNegocio) -> str:
    """«Adelante» si recupera en ≤ 12 meses, riesgo ≤ 3 y madurez ≥ 3; «Piloto acotado» si recupera en ≤ 24 meses
    y madurez ≥ 2; «No recomendado» en otro caso."""
    raise NotImplementedError("Completa este bloque")


def resumen(c: CasoNegocio) -> str:
    meses = meses_recuperacion(c)
    return (f"{c.nombre}: beneficio {beneficio_mensual(c)} €/mes · recuperación "
            f"{'nunca' if math.isinf(meses) else f'{meses} meses'} · ROI año 1 {roi_primer_anio(c)} % · {recomendacion(c)}")


if __name__ == "__main__":
    # Informe semanal de PMO Copilot: 119 min ahorrados × 4 semanas × 6 jefes de proyecto, 45 €/h.
    pmo = CasoNegocio("PMO Copilot", 119 / 60 * 4 * 6, 45, 18_000, 250, riesgo=2, madurez_datos=4)
    print(resumen(pmo))
