"""Sesión 12 - Ejercicio 3: validación del documento generado (reglas + LLM como juez + muestreo humano).

    python sesion_12_documentacion/ejercicios/s12_ej3_validacion.py
"""

from __future__ import annotations

import random
import re
import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402
from s12_ej2_generacion import SECCIONES  # noqa: E402


class Juicio(BaseModel):
    puntuacion: int = Field(ge=1, le=5, description="1 = inaceptable, 5 = excelente")
    cumple: bool
    motivos: list[str]


def comprobaciones(informe: str, completados: int, comprometidos: int) -> list[dict]:
    """Comprobaciones deterministas. Una fila ``{"comprobacion", "ok", "detalle"}`` por cada una:

    1. «secciones»: las seis ``SECCIONES`` aparecen como títulos ``## `` y en orden.
    2. «semaforo»: los colores de la tabla de semáforo son todos Verde, Ámbar o Rojo.
    3. «cifras»: aparece «<completados> de <comprometidos> puntos».
    4. «resumen_tres_lineas»: la sección 1 tiene exactamente tres líneas no vacías.
    """
    raise NotImplementedError("Completa este bloque")


RUBRICA = ("Evalúa el informe de estado frente a los datos de origen: (1) todas las cifras coinciden con los datos; "
           "(2) no afirma nada que no esté en los datos; (3) el resumen es claro para un director; "
           "(4) los riesgos que hay que escalar están señalados.")


def juzgar(informe: str, datos_origen: str, rubrica: str = RUBRICA) -> Juicio:
    """LLM como juez con salida estructurada ``Juicio`` (temperatura 0)."""
    raise NotImplementedError("Completa este bloque")


def muestra_revision(elementos: list[str], porcentaje: float, semilla: int = 42, minimo: int = 1) -> list[str]:
    """Muestra aleatoria reproducible para revisión humana: ``max(minimo, ceil(n × porcentaje / 100))`` elementos
    (sin superar n), conservando el orden original."""
    raise NotImplementedError("Completa este bloque")


def informe_validacion(nombre: str, filas: list[dict], juicio: Juicio | None) -> str:
    """Markdown: «## Validación de <nombre>», tabla | Comprobación | Resultado | Detalle | (✅ / ❌) y, si hay juicio,
    «Juez: <puntuación>/5 · cumple: sí|no» seguido de los motivos en viñetas. Termina con «Veredicto: APTO» si todas
    las comprobaciones pasan y el juez (si lo hay) dice que cumple; si no, «Veredicto: REVISIÓN HUMANA»."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    from s12_ej2_generacion import DATOS_EJEMPLO, generar_informe, resumen_con_llm

    informe = generar_informe(DATOS_EJEMPLO, resumen_con_llm(DATOS_EJEMPLO))
    filas = comprobaciones(informe, DATOS_EJEMPLO.completados, DATOS_EJEMPLO.comprometidos)
    juicio = juzgar(informe, repr(DATOS_EJEMPLO))
    print(informe_validacion("informe semanal Faro 2.0", filas, juicio))
    print("\nMuestra para revisión humana (20 % de 12 actas):", muestra_revision([f"acta_{i}" for i in range(12)], 20))
